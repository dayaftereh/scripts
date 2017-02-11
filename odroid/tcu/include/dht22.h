#ifndef DHT22_H
#define DHT22_H

// -----------------------------------------------

#include <stdio.h>
#include <wiringPi.h>

#include "config.h"

// -----------------------------------------------

#define DHT22_BITS 40
#define DHT22_FACTOR 10.0f
#define DHT22_MAX_TIMES	85
#define DHT22_MAX_COUNTER	255

// -----------------------------------------------

typedef enum {
  DHT22_OK,
  DHT22_NO_PULLUP,
  DHT22_NO_DATA,
  DHT22_BAD_CRC,
} DHT22ErrorCode;

// -----------------------------------------------

DHT22ErrorCode dht22_check_pull_up(struct Config *config);
DHT22ErrorCode dht22_read(struct Config *config, float *humidity, float *temperature);

// -----------------------------------------------

#endif /* DHT22_H */
