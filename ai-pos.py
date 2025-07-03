import cv2
from ultralytics import YOLO
import serial
import time
import tkinter as tk

# === CONFIGURATION ===
MODEL_PATH = "/home/aipos/Desktop/my_model.pt"
LABELS_PATH = "/home/aipos/Desktop/items.txt"
UIDS_PATH = "/home/aipos/Desktop/authorized_uids.txt"
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600
CONFIDENCE_THRESHOLD = 0.4
IMAGE_SIZE = 416

# === LOAD MODEL AND DATA ===
model = YOLO(MODEL_PATH)
item_prices = {}
with open(LABELS_PATH, "r") as f:
    for line in f:
        if "," in line:
            name, price = line.strip().split(",")
            item_prices[name.upper()] = float(price)

authorized_uids = set()
with open(UIDS_PATH, "r") as f:
    for line in f:
        uid = line.strip().upper()
        if uid:
            authorized_uids.add(uid)

# === GLOBAL STATE ===
total_price = 0.0
all_items = []

# === LOGIC FUNCTIONS ===
def detect_items():
    global total_price, all_items
    cap = cv2.VideoCapture("rtsp://admin:0569AHMAD@pos@169.254.72.234/Streaming/Channels/101", cv2.CAP_FFMPEG)
    if not cap.isOpened():
        update_status("❌ Failed to open camera.")
        return

    screen_res = (1920, 1080)
    while True:
        ret, frame = cap.read()
        if not ret:
            update_status("⚠️ Camera error")
            break

        frame_resized = cv2.resize(frame, screen_res)
        cv2.namedWindow("Live Feed", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Live Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Live Feed", frame_resized)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            results = model.predict(source=frame, imgsz=IMAGE_SIZE, conf=CONFIDENCE_THRESHOLD)
            cap.release()
            cv2.destroyAllWindows()
            labels = [model.names[int(cls)] for cls in results[0].boxes.cls]
            detected = list(set(label.upper() for label in labels))
            if not detected:
                update_status("No items detected.")
                return
            display_lines = []
            for item in detected:
                price = item_prices.get(item, 0)
                total_price += price
                all_items.append(item)
                display_lines.append(f"- {item}: {price:.2f}₪")
            display_lines.append(f"\n🧾 Current total: {total_price:.2f}₪")
            update_status("\n".join(display_lines))
            return
        elif key == 27:
            cap.release()
            cv2.destroyAllWindows()
            return

def wait_for_valid_rfid():
    global total_price
    update_status("📡 Waiting for your flag...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except:
        update_status("❌ Failed to connect to Arduino.")
        return

    timeout = time.time() + 20
    while time.time() < timeout:
        root.update()
        line = ser.readline().decode(errors="ignore").strip().upper()
        if line.startswith("UID:"):
            uid = line.replace("UID:", "").strip()
            if uid in authorized_uids:
                ser.write(b"OPEN\n")
                update_status("🇵🇸 Welcome to our market!\n✅ Payment accepted.")
                return
            else:
                update_status("❌ UID not authorized.")
                return
    update_status("⏱️ RFID Timeout.")

# === GUI FUNCTIONS ===
def update_status(msg):
    status_label.config(text=msg)
    status_label.update_idletasks()

def handle_scan():
    root.withdraw()
    detect_items()
    root.deiconify()

def handle_pay():
    update_status("📡 Waiting for your flag...")
    wait_for_valid_rfid()

def handle_exit():
    root.destroy()

# === GUI SETUP ===
root = tk.Tk()
root.title("AI POS System")
root.attributes("-fullscreen", True)

frame = tk.Frame(root)
frame.pack(expand=True)

btn_font = ("Arial", 24)
tk.Button(frame, text="Scan Items", font=btn_font, command=handle_scan, width=20, height=2).pack(pady=20)
tk.Button(frame, text="Add More Items", font=btn_font, command=handle_scan, width=20, height=2).pack(pady=20)
tk.Button(frame, text="Pay", font=btn_font, command=handle_pay, width=20, height=2).pack(pady=20)
tk.Button(frame, text="Exit", font=btn_font, command=handle_exit, width=20, height=2).pack(pady=20)

status_label = tk.Label(root, text="Welcome to AI POS", font=("Arial", 20), wraplength=1200, justify="left")
status_label.pack(pady=30)

root.mainloop()
