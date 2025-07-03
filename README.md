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
