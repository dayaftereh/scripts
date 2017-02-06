#ifndef CONFIG_H
#define CONFIG_H

// -----------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// -----------------------------------------------

#define CONFIG_DELIM "="
#define CONFIG_COMMENT "#"
#define CONFIG_LINE_BUF_LEN 1024

// -----------------------------------------------

struct Config {
  int fan_pin;
  int dht22_pin;
  int gpio_mode;
  int fan_runtime;
  float tmu_threshold;
  float dht22_threshold;
  char tmu_file[CONFIG_LINE_BUF_LEN];
};

// -----------------------------------------------

typedef enum {
  CONFIG_OK,
  CONFIG_ERROR
} ConfigError;

// -----------------------------------------------

char * config_deblank(char *str);
ConfigError config_read(const char *file, struct Config *config);

// -----------------------------------------------

#endif /* CONFIG_H */
