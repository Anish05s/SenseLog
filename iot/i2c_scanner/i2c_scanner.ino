// ================================================
// i2c_scanner.ino
// Upload this to Arduino Uno FIRST
// It will tell you exactly what's connected
// ================================================

#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("\nI2C Scanner Starting...");
}

void loop() {
  byte error, address;
  int devices = 0;

  Serial.println("Scanning...");

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("Device found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      devices++;
    }
  }

  if (devices == 0) {
    Serial.println("No I2C devices found ❌");
  } else {
    Serial.println("Scan complete ✅");
  }

  delay(3000);
}
