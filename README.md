# 🎯 Web Browser Based Remote and Autonomous Face Tracking
## Designed for Crunchlabs Hack Pack IR Turret (by Mark Rober) 
### Using Raspberry Pi Zero 2 W + Camera Module 3 
**Repo:** [`ir_turret_browser`](https://github.com/martyn-johnson/ir_turret_browser)

---

## 🧪 Overview

A lightweight, browser-driven face-tracking turret system that offloads real-time AI processing to the client device. The Raspberry Pi Zero 2 W provides the live camera feed and serial communication to the Arduino, while the browser handles all face detection and tracking using TensorFlow.js — drastically reducing CPU usage on the Pi.

---

## 🚀 Features

- 📷 **Live MJPEG video** from Raspberry Pi Camera Module 3
- 🧠 **Browser-based face tracking** using TensorFlow.js
- 🎯 Mobile-first web UI with D-Pad, Fire, and Preferences
- 🔧 **Calibrate Target Zone** by tapping on the video stream
- 🔌 Serial communication with IR Turret Arduino (USB)

---

## 🏗️ System Architecture

```
Pi Camera → Flask MJPEG stream (/video_feed)
                          ↓
         Browser receives MJPEG stream in <img>
                          ↓
      TensorFlow.js detects faces on each frame
                          ↓
     Sends smart control commands to Flask (/command)
                          ↓
               Serial communication to Arduino
```

---

## 🧰 Hardware Requirements

- Raspberry Pi Zero 2 W (or better)
- Pi Camera Module 3 (Wide recommended)
- Crunchlabs Hack Pack IR Turret (by Mark Rober)
- Arduino with servo control sketch
- MicroSD card (16GB+), Wi-Fi configured

---

## ⚙️ Setup (Raspberry Pi)

### 1. Flash Raspberry Pi OS Lite (64-bit)
- Enable SSH, set hostname to `ir-turret.local`
- Pre-configure Wi-Fi and credentials

### 2. SSH Into the Pi

```bash
ssh pi@ir-turret.local
```

### 3. Update + Install Dependencies

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git python3-flask python3-serial python3-picamera2 serial-tools
```

### 4. Clone the Project

```bash
cd ~
git clone https://github.com/martyn-johnson/ir_turret_browser.git
cd ir_turret_browser
```

### 5. Test Camera

```bash
libcamera-hello
```

### 6. Run the App

```bash
python3 app.py
```

Then visit:

```
http://ir-turret.local:5000/
```

---

## 🧠 AI Offloading Benefits

This version shifts all face tracking and computer vision to the browser using TensorFlow.js — enabling smoother performance, less heat on the Pi, and greater flexibility (modern phones/tablets can handle real-time tracking easily).

---

## 🛠️ Developed By

Martyn Johnson  
📦 [GitHub](https://github.com/martyn-johnson)  
🎥 [YouTube](https://www.youtube.com/@atexj)
