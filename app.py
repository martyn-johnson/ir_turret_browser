from flask import Flask, render_template, Response, request, jsonify
from picamera2 import Picamera2
from turret_serial import TurretSerial
import threading
import serial.tools.list_ports
import time

app = Flask(__name__)

# Start camera at high resolution (16:9)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"size": (1280, 720)},
    controls={"AfMode": 1}
))
picam2.start()

# Default camera controls
picam2.set_controls({
    "AwbEnable": True,
    "AeEnable": True,
    "Brightness": 0.2,
    "Contrast": 1.3,
    "Saturation": 0.8,
    "Sharpness": 1.0,
    "AfMode": 1
})

# Serial communication to Arduino
turret = TurretSerial('/dev/ttyACM0')

# Global targeting config
target_x, target_y = 320, 180  # Default center for 640x360 canvas
auto_track = False
auto_fire = False
lock = threading.Lock()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.1)  # 10 FPS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/command/<cmd>', methods=['GET'])
def send_command(cmd):
    with lock:
        print(f"[COMMAND] Sent to Arduino: {cmd}")
        turret.send(cmd)
    return jsonify(success=True, command=cmd)

@app.route('/calibrate', methods=['POST'])
def calibrate():
    global target_x, target_y
    data = request.get_json()
    target_x = int(data.get('x', 640))
    target_y = int(data.get('y', 360))
    print(f"[CALIBRATION] Target set to: ({target_x}, {target_y})")
    return jsonify(success=True, x=target_x, y=target_y)

@app.route('/settings', methods=['POST'])
def update_settings():
    global auto_track, auto_fire
    data = request.get_json()
    auto_track = data.get('track', False)
    auto_fire = data.get('auto_fire', False)
    print(f"[SETTINGS] Track: {auto_track}, Auto Fire: {auto_fire}")
    try:
        settings = {
            "Brightness": float(data.get("brightness", 0.2)),
            "Contrast": float(data.get("contrast", 1.3)),
            "Saturation": float(data.get("saturation", 0.8)),
            "Sharpness": float(data.get("sharpness", 1.0)),
            "AnalogueGain": float(data.get("gain", 1.0)),
        }
        print(f"[CAMERA] Applying settings: {settings}")
        picam2.set_controls(settings)
    except Exception as e:
        print(f"[ERROR] Failed to set camera settings: {e}")
    return jsonify(success=True)

@app.route('/serial_ports', methods=['GET'])
def list_serial_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    return jsonify(ports=ports)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
