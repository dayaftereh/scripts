#ifndef DHT22_H
#define DHT22_H

// -----------------------------------------------

#include <wiringPi.h>

#include "config.h"

// -----------------------------------------------

#define GPIO_MODE_PINS 0
#define GPIO_MODE 1
#define GPIO_MODE_SYS 2
#define GPIO_MODE_PHYS 3

// -----------------------------------------------

void gpio_initialize(struct Config *config);

// -----------------------------------------------

#endif /* DHT22_H */
