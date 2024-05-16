/* Lectura de acelerometro de 3 ejes
Fecha: 29-04-2024
V. 1.1.0 
Frecuencia de muestreo ADXL345 0.1Hz - 3.2kHz*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(); // ADXL345 Object

void setup() {
  Serial.begin(9600);
  if(!accel.begin()) { 
    Serial.println("ADXL345 no detectado.");
    while(1);
  }
}

void loop() {
  sensors_event_t event;
  accel.getEvent(&event);
  Serial.print("X: ");
  Serial.print(event.acceleration.x);
  Serial.print(",");

  Serial.print("Y: ");
  Serial.print(event.acceleration.y);
  Serial.print(",");

  Serial.print("Z: ");
  Serial.print(event.acceleration.z);
  Serial.print(",");

  Serial.print("m/s^2");
  delay(20);
}
