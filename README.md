# 🧠 SenseLog

**SenseLog** is an IoT-based system that gives physical objects **memory and awareness** using Arduino and a Python-powered dashboard.

It tracks how objects are used in real-time, logs interactions, and visualizes behavior — effectively **bridging the gap between the physical and digital world**.

----
that how it work 
## 🚀 Features.

* 📦 Detects object pickup and placement using multiple sensors
* 🧠 Logs interaction events with timestamps via serial communication
* 📊 Real-time dashboard for monitoring usage patterns
* 📷 ESP32-CAM live video streaming integration
* 🕒 Accurate time tracking using RTC module
* ⚡ Lightweight system that runs locally (no cloud dependency)

---

## 🧰 Hardware Used

* Arduino Uno
* ESP32-CAM
* HC-SR501 PIR Sensor (motion detection)
* HC-SR04 Ultrasonic Sensor (distance/object detection)
* I2C LCD Display (real-time status display)
* DS3231 RTC Module (accurate timestamps)

---

## 🏗️ Project Structure

```id="f8vi5j"
SenseLog/
│── iot/                  # Arduino & ESP32 firmware
│   ├── main_uno/
│   │    └── main_uno.ino
│   ├── i2c_scanner/
│   │    └── i2c_scanner.ino
│   ├── esp32cam/
│   │    └── esp32cam.ino
│
│── python/
│   ├── logger/
│   │    └── logger.py
│   ├── dashboard/
│   │    └── dashboard.py
│   └── webapp/           # Future Flask app
│       └── app.py
│
│── data/
│   └── events.csv
│
│── docs/
│   └── architecture.md
│
└── README.md
```

---

## ⚙️ How It Works

```id="gabmar"
Sensors (PIR + Ultrasonic) → Arduino Processing → Serial Communication → Python Logger → CSV Storage → Dashboard Visualization
                                                                             → (Future) Flask Web App
```

### Workflow:

1. 🧲 PIR sensor detects motion near the object
2. 📏 Ultrasonic sensor detects object presence/placement
3. 🔌 Arduino processes sensor data and determines events (pickup/placement)
4. 🕒 DS3231 RTC provides accurate timestamps
5. 📟 I2C LCD displays real-time system status
6. 🐍 Python logger reads serial data using `pyserial`
7. 📁 Events are stored in `events.csv`
8. 📊 Dashboard visualizes usage patterns
9. 📷 ESP32-CAM provides optional live video monitoring

---

## 🛠️ Tech Stack

* 🔌 Arduino (C/C++)
* 🐍 Python (`pyserial`, `pandas`)
* 🌐 HTML (auto-generated dashboard)
* 📷 ESP32-CAM (WiFi video streaming)

---

## ▶️ Getting Started

### 1. Clone the repository

```id="s6eg1l"
git clone https://github.com/YOUR_USERNAME/SenseLog.git
cd SenseLog
```

---

### 2. Install dependencies

```id="9mdjc4"
pip install pyserial pandas
```

---

### 3. Upload Arduino Code

* Open `main_uno/main_uno.ino` in Arduino IDE
* Select **Arduino Uno** and correct COM port
* Upload the code

(Optional)

* Use `i2c_scanner.ino` to verify I2C devices (LCD, RTC)

---

### 4. Run the Logger

```id="lgx7i4"
python python/logger/logger.py
```

---

### 5. Run the Dashboard

```id="q7j5kt"
python python/dashboard/dashboard.py
```

Open in browser:

```id="8ql47b"
http://localhost:5000
```

---

## 📊 Example Output

* Event logged:
  `Object picked at 14:32:10`
* Data stored in CSV
* Dashboard updates in near real-time

---

## 💡 Use Cases

* 🏠 Smart homes (object usage tracking)
* 📦 Inventory tracking systems
* 📊 Habit tracking & productivity monitoring
* 🧠 Assistive tech for memory support
* 🔬 Research in IoT + human behavior

---

## 📈 Future Improvements

* 🌐 Flask-based interactive web dashboard
* ☁️ Cloud database integration (Firebase / MongoDB)
* 📱 Mobile app support
* 🤖 AI-based usage prediction & anomaly detection
* 🔔 Smart alerts (unused / misplaced objects)

---

## ⚠️ Notes

* Ensure correct COM port is selected for serial communication
* ESP32-CAM requires stable power (avoid weak USB supply)
* Proper sensor calibration improves accuracy

---

## 🧑‍💻 Author

**Anish Sarkar & Arya Ghosh**
B.Tech CSE | IoT, AI/ML & Blockchain Enthusiasts

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to contribute!
