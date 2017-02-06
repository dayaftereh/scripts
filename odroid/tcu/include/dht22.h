#ifndef DHT22_H
#define DHT22_H

#include <stdio.h>
#include <wiringPi.h>
#include "config.h"


#define MODE 15
#define PIN 15
#define MAX_TIMINGS	85

typedef enum {
  DHT_OK,
  DHT_NO_PULLUP,
  DHT_NO_DATA,
  DHT_BAD_CRC,
} DHTErrorCode;

DHTErrorCode dht22_read(int pin, float *humidity, float *temperature);

#endif /* DHT22_H */
