# ================================================
# logger.py
# Reads events from Arduino Uno and saves to CSV
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
from datetime import datetime

# ---- CHANGE THIS TO YOUR ARDUINO COM PORT ----
# How to find it: Arduino IDE → Tools → Port
# It will say something like COM3 or COM5
PORT = "COM3"
# ----------------------------------------------

BAUD     = 9600
CSV_FILE = "events.csv"

def setup_csv():
    # Create the file with headers if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["object_id", "event_type", "timestamp"])
        print(f"Created {CSV_FILE}")

def main():
    setup_csv()

    print("=" * 40)
    print("  Objects That Remember — Logger")
    print("=" * 40)
    print(f"Connecting to Arduino on {PORT}...")

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print("Connected! Pick up your object to test.")
        print("Press Ctrl+C to stop.\n")
    except Exception as e:
        print(f"\nERROR: Could not connect to {PORT}")
        print("Fix: Check your COM port in Arduino IDE → Tools → Port")
        return

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)

        while True:
            try:
                # Read one line from Arduino
                raw = ser.readline().decode('utf-8').strip()

                # Only process lines that start with EVENT
                if raw.startswith("EVENT"):
                    parts = raw.split(",")

                    if len(parts) == 4:
                        _, obj_id, event_type, timestamp = parts

                        # Save to CSV
                        writer.writerow([obj_id, event_type, timestamp])
                        f.flush()  # write immediately, don't buffer

                        # Print nicely
                        icon = "📦 PICKED UP" if event_type == "PICKUP" else "📥 PUT DOWN"
                        print(f"{icon}  |  {obj_id}  |  {timestamp}")

            except KeyboardInterrupt:
                print("\nLogger stopped.")
                break
            except Exception as e:
                # Skip bad lines silently
                continue

if __name__ == "__main__":
    main()