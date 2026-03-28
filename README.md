# 🧠 SenseLog

**SenseLog** is an IoT-based system that gives physical objects **memory and awareness** using Arduino and a Python-powered dashboard.

It tracks how objects are used in real-time, logs interactions, and visualizes behavior — bridging the gap between the physical and digital world.

---

## 🚀 Features

* 📦 Detects object pickup and placement using sensors
* 🧠 Logs interaction events with timestamps
* 📊 Real-time dashboard for monitoring usage
* 📡 ESP32-CAM live video integration
* ⚡ Lightweight and runs locally (no cloud required)

---

## 🏗️ Project Structure

```
SenseLog/
│── iot/                  # Arduino & ESP32 firmware
│   ├── esp32cam/
│   │    └── esp32cam.ino
│   ├── main_uno/
│   │    └── main_uno.ino
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

```
Arduino → Serial Communication → Python Logger → CSV Storage → Dashboard Visualization
                                               → (Future) Flask Web App
```

1. Arduino detects object interaction
2. Sends event data via serial (USB)
3. Python logger records data into CSV
4. Dashboard reads CSV and displays insights
5. ESP32 streams live video feed

---

## 🛠️ Tech Stack

* 🔌 Arduino (C/C++)
* 🐍 Python (pyserial, pandas)
* 🌐 HTML (auto-generated dashboard)
* 📷 ESP32-CAM

---

## ▶️ Getting Started

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/SenseLog.git
cd SenseLog
```

---

### 2. Install dependencies

```
pip install pyserial pandas
```

---

### 3. Run the logger

```
python python/logger/logger.py
```

---

### 4. Run the dashboard

```
python python/dashboard/dashboard.py
```

Open in browser:

```
http://localhost:5000
```

---

## 📈 Future Improvements

* 🌐 Flask-based web dashboard
* ☁️ Cloud database (Firebase / MongoDB)
* 📱 Mobile app integration
* 🤖 AI-based usage prediction
* 🔔 Smart alerts for unused objects

---

## 💡 Use Cases

* Smart homes 🏠
* Inventory tracking 📦
* Habit tracking systems 📊
* Assistive tech for memory support 🧠
* Research in IoT + human behavior

---

## 🧑‍💻 Author

**Anish Sarkar**
B.Tech CSE Student | IoT & Blockchain Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!
