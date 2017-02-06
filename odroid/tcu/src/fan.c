#include "include/fan.h"

// ----------------------------------------------------------------------------

void fan_stop(struct Config *config){
  pinMode(config->fan_pin, OUTPUT);
  digitalWrite(config->fan_pin, LOW);
}

// ----------------------------------------------------------------------------

void fan_start(struct Config *config){
  pinMode(config->fan_pin, OUTPUT);
  digitalWrite(config->fan_pin, HIGH);
}
