#ifndef CTRL_H
#define CTRL_H

// -----------------------------------------------

#include <wiringPi.h>

#include "fan.h"
#include "tmu.h"
#include "dht22.h"
#include "config.h"

// -----------------------------------------------

#define CTRL_DELAY_TIME 3000

// -----------------------------------------------

extern volatile int RUNNING;
extern volatile int FAN_TIMER;

// -----------------------------------------------

void ctrl_run(struct Config *config, int verbose);

// -----------------------------------------------

#endif /* CTRL_H */
