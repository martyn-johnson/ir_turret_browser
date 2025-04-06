# 🎯 Web Browser Based Remote and Autonomous Face Tracking
## Designed for Crunchlabs Hack Pack IR Turret (by Mark Rober) 
### Using Raspberry Pi Zero 2 W + Camera Module 3 
**Repo:** [`ir_turret_browser`](https://github.com/martyn-johnson/ir_turret_browser)
**See it in action:** [`Mark Rober’s IR Turret AI Face Tracking`](https://youtu.be/RiZ3YAne5aI?si=kj3cuOjsDZClt6xQ)

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

## ⚙️ Software Requirements

- Raspberry Pi Imager (https://www.raspberrypi.com/software/)
- Arduino IDE (https://www.arduino.cc/en/software/) or Hack Pack Create Agent (https://ide.crunchlabs.com/editor/8718988640487)

### Arduino Code

Go to https://ide.crunchlabs.com/editor/8718988640487 or get the Arduino IDE (https://www.arduino.cc/en/software/) and we need to modify and add some code to the sketch.

Here are the settings I used for movement:

```bash
int pitchMoveSpeed = 3; //this variable is the angle added to the pitch servo to control how quickly the PITCH servo moves - try values between 3 and 10
int yawMoveSpeed = 90; //this variable is the speed controller for the continuous movement of the YAW servo motor. It is added or subtracted from the yawStopSpeed, so 0 would mean full speed rotation in one direction, and 180 means full rotation in the other. Try values between 10 and 90;
int yawStopSpeed = 90; //value to stop the yaw motor - keep this at 90
int rollMoveSpeed = 90; //this variable is the speed controller for the continuous movement of the ROLL servo motor. It is added or subtracted from the rollStopSpeed, so 0 would mean full speed rotation in one direction, and 180 means full rotation in the other. Keep this at 90 for best performance / highest torque from the roll motor when firing.
int rollStopSpeed = 90; //value to stop the roll motor - keep this at 90

int yawPrecision = 30; // this variable represents the time in milliseconds that the YAW motor will remain at it's set movement speed. Try values between 50 and 500 to start (500 milliseconds = 1/2 second)
int rollPrecision = 158; // this variable represents the time in milliseconds that the ROLL motor with remain at it's set movement speed. If this ROLL motor is spinning more or less than 1/6th of a rotation when firing a single dart (one call of the fire(); command) you can try adjusting this value down or up slightly, but it should remain around the stock value (160ish) for best results.

int pitchMax = 130; // this sets the maximum angle of the pitch servo to prevent it from crashing, it should remain below 180, and be greater than the pitchMin
int pitchMin = 50; // this sets the minimum angle of the pitch servo to prevent it from crashing, it should remain above 0, and be less than the pitchMax
```

Then, add this inside your existing loop() and outside the if (IrReceiver.decode()) block, so both IR and serial input can be handled independently.

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
- Use **Raspberry Pi Imager**:
  - Choose: Raspberry Pi OS Lite (64-bit)
  - Enable: SSH, set hostname to `ir-turret.local`
  - Set username to `pi` and create a password
  - Configure Wi-Fi to your network settings


### 2. SSH Into the Pi
Power up the Raspberry Pi (this might take some time on first boot), then open a terminal on your machine and connect to the Pi vis SSH.

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


### (Optional) Auto-Start Flask App on Boot

rather than starting the app manually, you can start the app as a service on every boot.

```bash
sudo nano /etc/systemd/system/turret.service
```

Paste the following:

```ini
[Unit]
Description=IR Turret Flask App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/ir_turret_browser
ExecStart=/usr/bin/python3 /home/pi/ir_turret_browser/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable turret.service
sudo systemctl start turret.service
```

To restart the service after editing Python files:

```bash
sudo systemctl restart turret.service
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

Originally this project [`ir_turret`](https://github.com/martyn-johnson/ir_turret) was built with the Pi controlling the Face detection and tracking with OpenCV, however the Pi was getting very hot.

This version shifts all face tracking and computer vision to the browser using TensorFlow.js — enabling smoother performance, less heat on the Pi, and greater flexibility (modern phones/tablets can handle real-time tracking easily).

---

## 🛠️ Developed By AtexJ
 
🎥 [YouTube](https://www.youtube.com/@atexj)
