# IR Turret with Browser-Based Face Tracking  
## Project Specification  
**Repo:** `ir_turret_browser`  
**Goal:** Offload AI from Raspberry Pi → Run in-browser face tracking

---

## 🎯 Project Objective

Create a web-based IR turret control system where:

- The **Raspberry Pi** handles only:
  - Video streaming via MJPEG (`/video_feed`)
  - Receiving commands from the browser
  - Sending commands to the Arduino via serial

- The **browser handles**:
  - Live face detection and tracking
  - Determining turret movement offsets
  - Sending control commands (via HTTP)

---

## 🧱 System Components

### Hardware

- Raspberry Pi Zero 2 W
- Camera Module 3 (Wide)
- Crunchlabs IR Turret (Arduino-based)
- USB cable for Pi ↔ Arduino serial

### Software Stack

| Layer        | Tech                      |
|--------------|---------------------------|
| Frontend     | HTML/CSS/JS + TensorFlow.js |
| AI Tracking  | TensorFlow.js (BlazeFace) |
| Backend      | Flask (Python)            |
| Serial Comm  | PySerial                  |
| Video Feed   | PiCamera2 + MJPEG stream  |

---

## 🔄 System Flow

```mermaid
graph TD
  A[Pi Camera Stream] --> B[MJPEG /video_feed]
  B --> C[<img> tag in Browser]
  C --> D[Canvas + TensorFlow.js]
  D --> E[Face Detection]
  E --> F[Command Offset Calculation]
  F --> G[AJAX: /command/XYZ]
  G --> H[Flask API]
  H --> I[Serial to Arduino]
  I --> J[Servo Control (Yaw, Pitch, Fire)]
```

---

## 🖥️ Web Interface (UI)

- **Video Feed:** `<img>` showing MJPEG stream
- **D-Pad Controls:** ← ↑ → ↓ movement buttons
- **FIRE Button:** Manual fire trigger
- **Checkboxes:**
  - ✅ Enable Face Tracking (browser-side)
  - ✅ Auto-Fire when face is centered
- **Calibrate:** Tap on image to set target zone
- **Preferences Panel:** Camera control, gain, serial port selector

---

## 📡 Command Protocol (Pi ⇄ Arduino)

| Command | Description        |
|---------|--------------------|
| LEFT    | Yaw left           |
| RIGHT   | Yaw right          |
| UP      | Pitch up           |
| DOWN    | Pitch down         |
| FIRE    | Trigger fire       |
| STOP    | Stop movement      |
| Xnn     | Adjust yaw offset  |
| Ynn     | Adjust pitch offset|

---

## 📋 Key Improvements from Original Project

| Feature                     | Old Project (`ir_turret`) | New Project (`ir_turret_browser`) |
|----------------------------|----------------------------|------------------------------------|
| Face Detection Location    | Pi (OpenCV)                | Browser (TensorFlow.js)           |
| CPU Usage (on Pi)          | High                       | Minimal                            |
| Responsiveness             | Medium                     | High (device dependent)            |
| MJPEG Source               | Pi Camera                  | Pi Camera (same)                   |
| Tracking Speed             | Limited by Pi              | Browser-accelerated (WebGL)        |

---

## 🧠 Targeting Logic

- Center of the frame is the **default target zone**
- User can tap to calibrate the center using `/calibrate`
- Browser compares face center to `target_x`, `target_y`
- If deviation is large:
  - Send `Xnn` and `Ynn` serial commands to realign
- If Auto-Fire is ON and face is in zone:
  - Sends `FIRE`, then pauses for 5 seconds

---

## 💡 Future Ideas

- Known face recognition (friendly vs unknown)
- Real-time scoring mode / gamification
- Multiple turret support
- WebRTC streaming instead of MJPEG
- Multi-face priority targeting
- Voice control (via browser)

---

## 📦 Repository Structure

```
ir_turret_browser/
│
├── app.py               # Flask app
├── turret_serial.py     # Serial communication logic
├── templates/
│   └── index.html       # Frontend UI
├── static/
│   ├── js/
│   │   └── face_tracker.js   # TensorFlow.js logic
├── README.md
└── PROJECT.md
```
