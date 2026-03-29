// ================================================
// main_uno.ino — FINAL VERSION
// No MPU library needed — uses Wire directly
// ================================================

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>

// ------------------ PINS ------------------
#define PIR_PIN   2
#define TRIG_PIN  3
#define ECHO_PIN  4

// ------------------ SETTINGS ------------------
#define BASELINE_CM   12
#define PICKUP_CM     25
#define COOLDOWN_MS 1500   // reduced for faster response

// ------------------ OBJECTS ------------------
LiquidCrystal_I2C lcd(0x27, 16, 2);
RTC_DS3231 rtc;

// ------------------ VARIABLES ------------------
unsigned long lastEventTime = 0;
bool objectPresent = true;
bool pirTriggered = false;

// ------------------ DISTANCE ------------------
float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  return duration * 0.034 / 2.0;
}

// ------------------ TIME FORMAT ------------------
String getTime(DateTime dt) {
  String s = "";
  if (dt.hour() < 10) s += "0"; s += dt.hour(); s += ":";
  if (dt.minute() < 10) s += "0"; s += dt.minute(); s += " ";
  if (dt.day() < 10) s += "0"; s += dt.day(); s += "/";
  if (dt.month() < 10) s += "0"; s += dt.month();
  return s;
}

// ------------------ EVENT ------------------
void sendEvent(String type, String timeStr) {
  Serial.println("EVENT,book," + type + "," + timeStr);

  lcd.clear();
  lcd.setCursor(0, 0);

  if (type == "PERSON")      lcd.print("Person detected");
  if (type == "PICKED_UP")   lcd.print("Book picked up");
  if (type == "PUT_DOWN")    lcd.print("Book put down");

  lcd.setCursor(0, 1);
  lcd.print(timeStr);
}

// ------------------ SETUP ------------------
void setup() {
  Serial.begin(9600);
  Wire.begin();

  pinMode(PIR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  lcd.init();
  lcd.backlight();

  if (!rtc.begin()) {
    lcd.print("RTC ERROR!");
    while (1);
  }

  // Uncomment ONCE → upload → comment again
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  lcd.print("System Ready");
  delay(2000);
  lcd.clear();
}

// ------------------ LOOP ------------------
void loop() {
  unsigned long now = millis();
  DateTime rtcNow = rtc.now();
  String timeStr = getTime(rtcNow);

  int pirVal = digitalRead(PIR_PIN);

  // -------- PERSON PRIORITY --------
  if (pirVal == HIGH && !pirTriggered && (now - lastEventTime) > COOLDOWN_MS) {
    pirTriggered = true;
    lastEventTime = now;
    sendEvent("PERSON", timeStr);

    delay(1500);   // ignore ultrasonic temporarily
    return;
  }

  if (pirVal == LOW) {
    pirTriggered = false;
  }

  // -------- ULTRASONIC --------
  float dist = getDistance();

  // PICKED UP
  if (objectPresent && dist > PICKUP_CM && dist < 200 &&
      (now - lastEventTime) > COOLDOWN_MS) {
    objectPresent = false;
    lastEventTime = now;
    sendEvent("PICKED_UP", timeStr);
  }

  // PUT DOWN
  if (!objectPresent && dist < BASELINE_CM &&
      (now - lastEventTime) > COOLDOWN_MS) {
    objectPresent = true;
    lastEventTime = now;
    sendEvent("PUT_DOWN", timeStr);
  }

  delay(200);
}
