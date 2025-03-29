from flask import Flask, render_template, Response, request, jsonify
from picamera2 import Picamera2
from turret_serial import TurretSerial
from io import BytesIO
import threading
import serial.tools.list_ports
import time

app = Flask(__name__)

# Initialize camera
try:
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(
        main={"size": (640, 360)},  # Lower resolution for performance
        controls={"AfMode": 1}
    ))
    picam2.start()

    # Set default camera controls
    picam2.set_controls({
        "AwbEnable": True,
        "AeEnable": True,
        "Brightness": 0.2,
        "Contrast": 1.3,
        "Saturation": 0.8,
        "Sharpness": 1.0,
        "AfMode": 1
    })
    camera_available = True
    print("[INFO] Camera initialized successfully.")
except Exception as e:
    print(f"[ERROR] Camera initialization failed: {e}")
    camera_available = False

# Initialize serial communication
turret = TurretSerial('/dev/ttyUSB0')  # Adjust if needed

# Global variables
target_x, target_y = 320, 180
auto_track = False
auto_fire = False
latest_command = None
lock = threading.Lock()
last_command_time = 0
command_interval = 0.2
dead_zone = 30

def send_directional_command(offset_x, offset_y):
    global last_command_time

    current_time = time.time()
    if current_time - last_command_time >= command_interval:
        with lock:
            if offset_x > 0:
                turret.send("RIGHT")
            elif offset_x < 0:
                turret.send("LEFT")
            if offset_y > 0:
                turret.send("DOWN")
            elif offset_y < 0:
                turret.send("UP")
        last_command_time = current_time

def generate_frames():
    """
    Efficient MJPEG streaming using Picamera2 with in-memory JPEGs.
    """
    if not camera_available:
        print("[INFO] Camera is not available. Video feed is disabled.")
        return

    stream = BytesIO()

    while True:
        try:
            stream.seek(0)
            stream.truncate()
            picam2.capture_file(stream, format='jpeg')
            frame = stream.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"[ERROR] Frame generation failed: {e}")
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if not camera_available:
        return jsonify(error="Camera not available"), 503
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/command/<cmd>', methods=['GET'])
def send_command(cmd):
    global latest_command
    with lock:
        latest_command = cmd
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

    # Apply camera settings
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
