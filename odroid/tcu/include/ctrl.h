#ifndef CTRL_H
#define CTRL_H

// -----------------------------------------------

#include <wiringPi.h>
#include <stdatomic.h>

#include "fan.h"
#include "tmu.h"
#include "dht22.h"
#include "config.h"

// -----------------------------------------------

#define CTRL_DELAY_TIME 5000
#define CTRL_FAN_RUNTIME_ADD 10000

// -----------------------------------------------

extern atomic_int RUNNING;
extern atomic_int VERBOSE;
extern atomic_int FAN_TIMER;

// -----------------------------------------------

void ctrl_run(struct Config *config);
void ctrl_start_fan(struct Config *config);

// -----------------------------------------------

#endif /* CTRL_H */
