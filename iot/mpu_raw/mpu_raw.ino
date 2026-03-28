// mpu_raw.ino
// Talks to MPU6050 directly — no library needed!
// Keep DS3231 unplugged for this test

#include <Wire.h>

#define MPU 0x68  // MPU6050 I2C address

void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(1000);

  // Wake up MPU6050 (it starts in sleep mode)
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to 0 = wake up
  Wire.endTransmission(true);

  delay(100);
  Serial.println("MPU6050 started!");
  Serial.println("Shake the board to see values change");
}

void loop() {
  // Request accelerometer data
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting register for accel data
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);  // request 6 bytes

  // Read raw values
  int16_t ax = Wire.read() << 8 | Wire.read();
  int16_t ay = Wire.read() << 8 | Wire.read();
  int16_t az = Wire.read() << 8 | Wire.read();

  // Convert to g (divide by 16384 for ±2g range)
  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;

  Serial.print("X: "); Serial.print(ax_g);
  Serial.print("  Y: "); Serial.print(ay_g);
  Serial.print("  Z: "); Serial.println(az_g);

  delay(500);
}
