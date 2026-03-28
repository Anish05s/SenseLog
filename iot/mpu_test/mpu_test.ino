// mpu_test.ino
// Unplug DS3231 temporarily, then upload this
// Just tests if MPU works alone at 0x68

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  Serial.println("Testing MPU6050...");

  if (!mpu.begin(0x68)) {  // force address 0x68
    Serial.println("MPU FAILED - not found at 0x68");
    while (1);
  }

  Serial.println("MPU FOUND at 0x68!");
  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  Serial.print("X:"); Serial.print(a.acceleration.x);
  Serial.print(" Y:"); Serial.print(a.acceleration.y);
  Serial.print(" Z:"); Serial.println(a.acceleration.z);

  delay(500);
}
