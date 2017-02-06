#include "include/config.h"

// ----------------------------------------------------------------------------

char * config_deblank(char *str)
{
  char *out = str;
  char *put = str;
  for(; *str != '\0'; ++str)
  {
    if(*str != ' ' && *str != '\n')
      *put++ = *str;
  }
  *put = '\0';

  return out;
}

size_t config_strlen(const char *str){
  return strlen(str) + 1;
}

// ----------------------------------------------------------------------------

void config_dispatch(struct Config *config, const char *key, const char *value){
  if(strncmp(CONFIG_COMMENT, key, strlen(CONFIG_COMMENT)) == 0){
    return;
  }

  if(strcmp(key, "FAN_PIN") == 0){
    config->fan_pin = atoi(value);
  } else if(strcmp(key, "DHT22_PIN") == 0){
    config->dht22_pin = atoi(value);
  } else if(strcmp(key, "GPIO_MODE") == 0){
    config->gpio_mode = atoi(value);
  } else if(strcmp(key, "TMU_FILE") == 0){
    strncpy(config->tmu_file, value, config_strlen(value));
  }else if(strcmp(key, "FAN_RUNTIME") == 0){
    config->fan_runtime = atoi(value);
  }else if(strcmp(key, "DHT22_THRESHOLD") == 0){
    config->dht22_threshold = atof(value);
  }else if(strcmp(key, "TMU_THRESHOLD") == 0){
    config->tmu_threshold = atof(value);
  }
}

// ----------------------------------------------------------------------------

ConfigError config_read(const char *file, struct Config *config){

  char line[CONFIG_LINE_BUF_LEN];

  FILE *fp = fopen(file, "r");
  if(fp == NULL){
    return CONFIG_ERROR;
  }

  while(fgets(line, CONFIG_LINE_BUF_LEN, fp)) {
    char *cfline = strstr((char *)line, CONFIG_DELIM);

    if(cfline == NULL){
      continue;
    }

    char *value_ptr = cfline + strlen(CONFIG_DELIM);
    int value_length = config_strlen(value_ptr);
    int key_length = strlen(line) - value_length;

    char key_raw[CONFIG_LINE_BUF_LEN] = {0};
    char value_raw[CONFIG_LINE_BUF_LEN] = {0};

    strncpy(key_raw, line, key_length);
    strncpy(value_raw, value_ptr, value_length);

    config_dispatch(config, config_deblank(key_raw), config_deblank(value_raw));
  }

  fclose(fp);
  return CONFIG_OK;
}
