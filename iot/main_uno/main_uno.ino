// ================================================
// main_uno.ino — FINAL VERSION
// No MPU library needed — uses Wire directly
// ================================================

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>

#define MPU 0x68  // MPU6050 address

LiquidCrystal_I2C lcd(0x27, 16, 2);
RTC_DS3231 rtc;

// Motion settings
const float THRESHOLD = 0.5;        // how much movement = pickup
const unsigned long COOLDOWN = 5000; // 5 sec between events
unsigned long lastEventTime = 0;
bool isPickedUp = false;

// ------------------------------------------------
void setupMPU() {
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0); // wake up
  Wire.endTransmission(true);
  delay(100);
}

float getTotalMovement() {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);

  int16_t ax = Wire.read() << 8 | Wire.read();
  int16_t ay = Wire.read() << 8 | Wire.read();
  int16_t az = Wire.read() << 8 | Wire.read();

  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;

  // Total acceleration minus gravity (1g)
  float total = sqrt(ax_g*ax_g + ay_g*ay_g + az_g*az_g) - 1.0;
  return abs(total);
}

// ------------------------------------------------
void setup() {
  Serial.begin(9600);
  Wire.begin();

  // LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0); lcd.print("Objects That");
  lcd.setCursor(0, 1); lcd.print("Remember v1.0");
  delay(2000);
  lcd.clear();

  // RTC
  if (!rtc.begin()) {
    lcd.setCursor(0, 0); lcd.print("RTC ERROR!");
    while (1);
  }
  // Uncomment once to set time, then comment out again
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  // MPU
  setupMPU();

  lcd.setCursor(0, 0); lcd.print("System Ready!");
  Serial.println("System Ready!");
  delay(1500);
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Waiting...");
}

// ------------------------------------------------
void loop() {
  float movement = getTotalMovement();
  unsigned long now = millis();
  DateTime rtcNow = rtc.now();
  String timeStr = getTime(rtcNow);

  // Detect PICKUP
  if (!isPickedUp &&
      movement > THRESHOLD &&
      (now - lastEventTime) > COOLDOWN) {

    isPickedUp = true;
    lastEventTime = now;

    Serial.println("EVENT,notebook-001,PICKUP," + timeStr);

    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Picked up!");
    lcd.setCursor(0, 1); lcd.print(timeStr);
  }

  // Detect PUTDOWN (still for 4 seconds)
  if (isPickedUp &&
      movement < 0.1 &&
      (now - lastEventTime) > 4000) {

    isPickedUp = false;
    lastEventTime = now;

    Serial.println("EVENT,notebook-001,PUTDOWN," + timeStr);

    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Last used:");
    lcd.setCursor(0, 1); lcd.print(timeStr);
  }

  delay(100);
}

// ------------------------------------------------
String getTime(DateTime dt) {
  String s = "";
  if (dt.hour()   < 10) s += "0"; s += dt.hour();   s += ":";
  if (dt.minute() < 10) s += "0"; s += dt.minute(); s += " ";
  if (dt.day()    < 10) s += "0"; s += dt.day();    s += "/";
  if (dt.month()  < 10) s += "0"; s += dt.month();
  return s;
}
