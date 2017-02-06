#include "include/dht22.h"

DHT22ErrorCode dht22_check_pull_up(struct Config *config){
  pinMode(config->dht22_pin, INPUT);
  delayMicroseconds(50);

  if(digitalRead(config->dht22_pin) == LOW) {
    return DHT22_NO_PULLUP;
  }

  return DHT22_OK;
}

// ----------------------------------------------------------------------------

DHT22ErrorCode dht22_read(struct Config *config, float *humidity, float *temperature){
  int j = 0;
  int counter = 0;
  int laststate = HIGH;
  int data[5] = {0};

  // ########################################

  pinMode(config->dht22_pin, OUTPUT);
  digitalWrite(config->dht22_pin, LOW);
  delay(18);

  // ########################################

  pinMode(config->dht22_pin, INPUT);

  // ########################################

  for (int i = 0; i < DHT22_MAX_TIMES; i++)	{
    counter = 0;
    while (digitalRead(config->dht22_pin) == laststate)	{
      counter++;
      if (counter == DHT22_MAX_COUNTER) {
        break;
      }
    }
    laststate = digitalRead(config->dht22_pin);

    if (counter == DHT22_MAX_COUNTER){
      break;
    }

    if ((i >= 4) && (i % 2 == 0)){
      data[j / 8] <<= 1;
      if ( counter > 100 ){
        data[j / 8] |= 1;
      }
      j++;
    }
  }

  // ########################################

  if(j < 40){
    return DHT22_NO_DATA;
  }

  if (data[4] != ((data[0] + data[1] + data[2] + data[3]) & 0xFF)){
    return DHT22_BAD_CRC;
  }

  // ########################################

  int raw_hum = ((int) data[0] << 8) + data[1];
  int raw_tmu = ((int) data[2] << 8) + data[3];

  if (data[2] & 0x80) {
    raw_tmu = -raw_tmu;
  }

  // ########################################

  *humidity = raw_hum / DHT22_FACTOR;
  *temperature = raw_tmu / DHT22_FACTOR;

  // ########################################

  return DHT22_OK;
}
