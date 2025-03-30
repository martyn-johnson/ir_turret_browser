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
- 🧠 **Browser-based face detection and tracking** using TensorFlow.js
- 🎯 Mobile-first web UI with D-Pad, Fire, and Preferences
- 🔧 **Calibrate Target Zone** by tapping on the video stream
- 🔌 Serial communication with IR Turret Arduino (USB)
- ⚙️ **Adjustable Camera Settings** (brightness, contrast, saturation, etc.)
- 🔄 **Serial Port Selection** via dropdown in the web UI

---

## 🏗️ System Architecture

```
Pi Camera → Flask MJPEG stream (/video_feed)
                          ↓
         Browser receives MJPEG stream
                          ↓
         Manual Browser remote controls
                          ↓
      TensorFlow.js detects faces on each frame
                          ↓
     Sends smart control commands to Flask (/command)
                          ↓
               Serial communication to Arduino
```

---

## 🧰 Hardware Requirements

- Raspberry Pi Zero 2 W
- Pi Camera Module 3 (Wide recommended)
- Crunchlabs Hack Pack IR Turret (by Mark Rober)
- MicroSD card (16GB+), Wi-Fi configured
- USB A to microB cable (to power the Pi from the battery pack)
- Micro-B USB to USB A female cable (power and serial comms from the Pi to the Arduino)

---

## ⚙️ Setup (Raspberry Pi)

### Arduino Code

Go to https://ide.crunchlabs.com/editor/8718988640487 or get the Arduino IDE (https://www.arduino.cc/en/software/) and we need to add some code to the sketch.

I reduced the Yaw values to improve precision:

```bash
int yawMoveSpeed = 40;    // Reduce speed (from 90 to 40)
int yawPrecision = 80;    // Reduce duration (from 150 to 80)
```

Add this inside your existing loop() and outside the if (IrReceiver.decode()) block, so both IR and serial input can be handled independently.

```bash
// Check for serial input from Raspberry Pi
if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n'); // Read full command line
    cmd.trim(); // Remove whitespace or newlines

    if (cmd == "UP") {
        upMove(1);
    } else if (cmd == "DOWN") {
        downMove(1);
    } else if (cmd == "LEFT") {
        leftMove(1);
    } else if (cmd == "RIGHT") {
        rightMove(1);
    } else if (cmd == "FIRE") {
        fire();
    } else if (cmd == "FIREALL") {
        fireAll();
    } else if (cmd == "YES") {
        shakeHeadYes(3);
    } else if (cmd == "NO") {
        shakeHeadNo(3);
    } else {
        Serial.print("Unknown command: ");
        Serial.println(cmd);
    }
}
```

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

## 🔧 Web UI Features

### Preferences Panel
- **Track Faces**: Enable/disable automatic face tracking.
- **Auto Fire**: Enable/disable automatic firing when a face is detected.
- **Camera Settings**: Adjust brightness, contrast, saturation, sharpness, and gain (ISO).
- **Serial Port Selection**: Choose the correct serial port for Arduino communication.

### Calibration
- Tap on the video feed to set the target zone for the turret.
- The target zone is marked with crosshairs.

---

## 🧠 AI Offloading Benefits

This version shifts all face tracking and computer vision to the browser using TensorFlow.js — enabling smoother performance, less heat on the Pi, and greater flexibility (modern phones/tablets can handle real-time tracking easily).

---

## 🛠️ Developed By AtexJ
 
🎥 [YouTube](https://www.youtube.com/@atexj)
