# AI-POS: AI-Based Point of Sale System 💡💳

An AI-powered POS system that uses object detection and NFC authentication to fully automate the checkout experience.

## 🔧 Features

- 🎯 **Item Recognition** using YOLOv8 object detection
- 💳 **NFC Payment** integration with PN532 module
- 🧠 **Custom AI Model Training** using Roboflow and Ultralytics
- 🎥 **Live Camera Feed** for item scanning (Hikvision camera)
- 🧾 **Real-Time Cost Calculation** and GUI (Tkinter)
- 🧍 **RFID Authentication** with Arduino + Raspberry Pi
- 🔐 **Servo Gate Control** based on payment validation
- 🌟 **LED Feedback**: Green for success, Red for failure

## 📷 System Components

- Raspberry Pi 4 / 5
- Arduino (for RFID control)
- PN532 NFC Module
- Hikvision Camera
- Servo Motor + LEDs
- OLED Display (for item + cost display)

## 🧠 AI Model

- Trained with custom dataset using **Roboflow**
- YOLOv8 architecture
- 4 Item Classes: `laban`, `siniora_mortadella`, `top_time_chips`, `water_viviane`
- Exported formats: `.pt`, `.onnx`, `.tflite`

## 🖥️ GUI

- Built using Python's `Tkinter`
- Features: Scan Items, Add More Items, Pay with NFC


## 🧠 HOW TO USE

- First take a lot of photos for your items (alone + togethers)
- then upload your photos to Roboflow and label them then export them as yolo dataset
- use the steps in traincode.txt in colab to train the model 
- then export your model and put it on raspberry pi 
- connect the hardware then upload arduino code ard_code.ino
- use ai-pos.py to run the model on rapberry 
- you can use my ready trained model with its dataset


## 📸 Screenshots

![image](https://github.com/user-attachments/assets/b4529654-c63e-44a2-b7b6-c441cfc85b9d)
![image](https://github.com/user-attachments/assets/a5cac74e-74ed-4cea-b785-8fba1749df03)

## 📜 License
This project is open source and free for any one to use.

## 🙋‍♂️ Author
Ahmad Hmied

📧 ahmadkhmied@gmail.com

🌍 Tuqu', Bethlehem, Palestine


