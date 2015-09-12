#include <Wire.h>
#include "Adafruit_MPR121.h"

Adafruit_MPR121 capacitive_touch_sensor = Adafruit_MPR121();

uint16_t last_touch_state = -1;
uint8_t light_pins[] = {3, 5, 6, 9};
float light_brightnesses[] = {0.0, 0.0, 0.0, 0.0};

void setup() {
  // initialize PRNG with value of disconnected analog pin, to get a good random seed
  randomSeed(analogRead(0));
  
  // set up pins
  for (uint8_t i = 0; i < sizeof(light_pins) / sizeof(light_pins[0]); i ++) {
    pinMode(light_pins[i], OUTPUT);
  }

  while (!Serial); // wait for the Serial library to be ready
  Serial.begin(9600);
  if (!capacitive_touch_sensor.begin(0x5A)) { // default shield address is 0x5A
    Serial.println("TOUCH SHIELD NOT FOUND");
    while (1);
  }
}

void loop() {
  // send out any touch information
  uint16_t touch_state = capacitive_touch_sensor.touched();
  if (touch_state != last_touch_state) {
    // set a random light's brightness to max if a new light was touched
    if ((touch_state & ~last_touch_state) != 0) {
      light_brightnesses[random(4)] = 1.0;
    }
    
    Serial.println(touch_state);
    
    last_touch_state = touch_state;
  }

  // step the lights
  for (uint8_t i = 0; i < sizeof(light_pins) / sizeof(light_pins[0]); i ++) {
    light_brightnesses[i] *= 0.997;
    analogWrite(light_pins[i], (int)(light_brightnesses[i] * 255) + 1);
  }
}

