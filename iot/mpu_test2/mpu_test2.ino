// mpu_test2.ino
// Uses "MPU6050 by Electronic Cats" library
// Keep DS3231 unplugged for this test

#include <Wire.h>
#include <MPU6050_tockn.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(1000);

  Serial.println("Initializing MPU6050...");
  mpu.initialize();

  if (mpu.testConnection()) {
    Serial.println("MPU6050 CONNECTED SUCCESSFULLY!");
  } else {
    Serial.println("MPU6050 connection FAILED");
  }
}

void loop() {
  if (mpu.testConnection()) {
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    Serial.print("X:"); Serial.print(ax);
    Serial.print(" Y:"); Serial.print(ay);
    Serial.print(" Z:"); Serial.println(az);
  }
  delay(500);
}
