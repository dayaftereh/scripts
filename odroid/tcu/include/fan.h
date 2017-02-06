#ifndef FAN_H
#define FAN_H

// -----------------------------------------------

#include <wiringPi.h>

#include "config.h"

// -----------------------------------------------

void fan_stop(struct Config *config);
void fan_start(struct Config *config);

// -----------------------------------------------

#endif /* FAN_H */
