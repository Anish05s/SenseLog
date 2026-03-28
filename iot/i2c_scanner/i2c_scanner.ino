// ================================================
// i2c_scanner.ino
// Upload this to Arduino Uno FIRST
// It will tell you exactly what's connected
// ================================================

#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("Scanning I2C bus...");
  Serial.println("-------------------");

  int found = 0;

  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("Found device at address: 0x");
      if (addr < 16) Serial.print("0");
      Serial.print(addr, HEX);

      // Tell user what each address likely is
      if (addr == 0x27) Serial.print("  → This is your LCD");
      if (addr == 0x3F) Serial.print("  → This is your LCD (alternate address)");
      if (addr == 0x68) Serial.print("  → This is MPU-6050 (AD0 LOW) or DS3231");
      if (addr == 0x69) Serial.print("  → This is MPU-6050 (AD0 HIGH) ✓ correct");
      if (addr == 0x57) Serial.print("  → This is DS3231 EEPROM");

      Serial.println();
      found++;
    }
  }

  Serial.println("-------------------");
  if (found == 0) {
    Serial.println("Nothing found! Check your SDA/SCL wiring.");
  } else {
    Serial.print("Total devices found: ");
    Serial.println(found);
  }
  Serial.println("Expected: 0x27 (LCD), 0x57 (RTC), 0x68 (RTC), 0x69 (MPU)");
}

void loop() {
  // nothing — just runs once
}
