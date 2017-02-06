#include "include/gpio.h"

// ----------------------------------------------------------------------------

void gpio_initialize(struct Config *config){
  switch(config->gpio_mode){
    case GPIO_MODE_PINS:
      wiringPiSetup();
      return;
    case GPIO_MODE:
      wiringPiSetupGpio();
      return;
    case GPIO_MODE_SYS:
      wiringPiSetupSys();
      return;
    case GPIO_MODE_PHYS:
      wiringPiSetupPhys();
      return;
  }
}
