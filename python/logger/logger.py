# ================================================
# logger.py - Objects That Remember
# Reads events from Arduino Uno, saves to CSV and grabs snapshots
# ================================================
# First run this in terminal/cmd:
#   pip install pyserial pandas
#
# Then run:
#   python logger.py
# ================================================

import serial
import csv
import os
import requests
import time
from datetime import datetime

PORT     = "COM3"          # Arduino Uno port
BAUD     = 9600
CSV_FILE = "events.csv"
ESP32_IP = "192.168.1.37"  # change to your ESP32-CAM IP
SNAP_DIR = "snapshots"

def setup():
    # Create CSV with headers if needed
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["object_id", "event_type", "timestamp"])
        print(f"Created {CSV_FILE}")
    # Create snapshots folder
    if not os.path.exists(SNAP_DIR):
        os.makedirs(SNAP_DIR)
        print(f"Created {SNAP_DIR}/")

def grab_snapshot(timestamp):
    # Capture a photo from ESP32-CAM
    try:
        url = f"http://{ESP32_IP}/capture"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            fname = timestamp.replace(":", "-").replace(" ", "_") + ".jpg"
            path  = os.path.join(SNAP_DIR, fname)
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"  Snapshot saved: {fname}")
    except Exception as e:
        print(f"  Snapshot failed: {e}")

def main():
    setup()

    print("=" * 42)
    print("  Objects That Remember - Logger v2")
    print("=" * 42)
    print(f"Connecting to Arduino on {PORT}...")

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print("Connected!")
        print("Waiting for events... (Ctrl+C to stop)\n")
    except Exception:
        print(f"\nERROR: Could not connect to {PORT}")
        print("Fix: Close Arduino Serial Monitor first!")
        return

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        while True:
            try:
                raw = ser.readline().decode('utf-8').strip()
                if raw.startswith("EVENT"):
                    parts = raw.split(",")
                    if len(parts) == 4:
                        _, obj_id, event_type, timestamp = parts
                        writer.writerow([obj_id, event_type, timestamp])
                        f.flush()

                        # Print event
                        label = {
                            "PICKED_UP": "PICKED UP",
                            "PUT_DOWN":  "PUT DOWN ",
                            "PERSON":    "PERSON   "
                        }.get(event_type, event_type)
                        print(f"[{timestamp}] {label} | {obj_id}")

                        # Grab snapshot on pickup or person detected
                        if event_type in ["PICKED_UP", "PERSON"]:
                           time.sleep(1)   # give ESP32 time
                           grab_snapshot(timestamp)

            except KeyboardInterrupt:
                print("\nLogger stopped.")
                break
            except Exception:
                continue

if __name__ == "__main__":
    main()
