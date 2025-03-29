import serial
import threading
import time

class TurretSerial:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.lock = threading.Lock()
        self._connect()

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Allow time for Arduino to reboot
            print(f"[SERIAL] Connected to Arduino on {self.port}")
        except Exception as e:
            print(f"[ERROR] Could not connect to Arduino on {self.port}: {e}")
            self.ser = None

    def send(self, cmd):
        if not self.ser or not self.ser.is_open:
            self._connect()
        if self.ser and self.ser.is_open:
            with self.lock:
                message = (cmd + '\n').encode('utf-8')
                self.ser.write(message)
                print(f"[SERIAL] Sent: {cmd}")
        else:
            print(f"[SERIAL] Skipped sending (not connected): {cmd}")
