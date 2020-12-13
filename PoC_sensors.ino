#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define SEALEVELPRESSURE_HPA (1018)

Adafruit_BME680 bme;

const int InPin = 4;  // Analog input pin that the potentiometer is attached to
const int brocheSortie = 18; // LED branchée à GPIO 18

int sensorValue = 0;        // value read from the pot


void setup() {

ledcAttachPin(brocheSortie, 0); //broche 18 associée au canal PWM 0
ledcSetup(0, 5000, 12); // canal = 0, frequence = 5000 Hz, resolution = 12 bits
pinMode(InPin, INPUT);
Serial.begin(9600);
while (!Serial);
Serial.println(F("BME680 test"));

if (!bme.begin()) {
Serial.println("Could not find a valid BME680 sensor, check wiring!");
while (1);
}

// Set up oversampling and filter initialization
bme.setTemperatureOversampling(BME680_OS_8X);
bme.setHumidityOversampling(BME680_OS_2X);
bme.setPressureOversampling(BME680_OS_4X);
bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
bme.setGasHeater(320, 150); // 320*C for 150 ms
}

void loop() {
if (! bme.performReading()) {
Serial.println("Failed to perform reading :(");
return;
}
sensorValue = analogRead(InPin);

if(bme.gas_resistance >= 160000) {
ledcWrite(0, 200);
}
if(bme.gas_resistance >= 150000 && bme.gas_resistance <= 160000) {
ledcWrite(0, 2000);
}
if(bme.gas_resistance <= 150000) {
ledcWrite(0, 4095);
}
  // print the results to the Serial Monitor:
Serial.println(bme.temperature);

Serial.println(bme.humidity);

Serial.println(bme.gas_resistance);

Serial.println(sensorValue);

delay(1000);
}
