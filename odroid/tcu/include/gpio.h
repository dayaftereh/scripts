#ifndef GPIO_H
#define GPIO_H

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

#endif /* GPIO_H */
