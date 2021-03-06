#include "include/ctrl.h"

// ----------------------------------------------------------------------------

void ctrl_update_tmu(struct Config *config){
  float tmu;
  if(tmu_read(config, &tmu) != TMU_OK){
    fprintf(stderr, "tmu :: can't read temperature from in-build file\n");
    return;
  }

  if(VERBOSE){
    printf( "tmu :: temperature [ %.1f C ]\n", tmu);
  }

  if(tmu > config->tmu_threshold && FAN_TIMER <= 0){
    printf( "tmu :: reached temperature threshold [ %.1f C > %.1f C ]\n", tmu, config->tmu_threshold);
    ctrl_start_fan(config);
  }
}

void ctrl_update_dht22(struct Config *config){
  float humidity;
  float temperature;

  if(dht22_read(config, &humidity, &temperature) != DHT22_OK){
    fprintf(stderr, "dht22 :: can't read temperature from sensor\n");
    return;
  }

  if(VERBOSE){
    printf("dht22 :: temperature [ %.1f C ]\n", temperature);
  }

  if(temperature > config->dht22_threshold && FAN_TIMER <= 0){
    printf("dht22 :: reached temperature threshold [ %.1f > %.1f ]\n", temperature, config->dht22_threshold);
    ctrl_start_fan(config);
  }
}

// ----------------------------------------------------------------------------

void ctrl_start_fan(struct Config *config){
  FAN_TIMER = config->fan_runtime;
  printf( "ctrl :: fan has been started for [ %d ms ]\n", config->fan_runtime);
}

void ctrl_update_fan(struct Config *config, int delta) {
  if(FAN_TIMER <= 0){
    return;
  }

  fan_start(config);
  FAN_TIMER -= delta;

  if(FAN_TIMER <= 0) {
    fan_stop(config);
    printf( "ctrl :: fan stopped, because run timer has been expired\n");
  }
}

// ----------------------------------------------------------------------------

int ctrl_calc_delta(int *last_update){
  int delta = millis() - *last_update;
  *last_update = millis();
  return delta;
}

// ----------------------------------------------------------------------------

void ctrl_run(struct Config *config){
  printf("ctrl :: started\n");

  int last_update = millis();
  FAN_TIMER = config->fan_runtime;

  while(RUNNING){
    ctrl_update_tmu(config);
    ctrl_update_dht22(config);

    int delta = ctrl_calc_delta(&last_update);
    ctrl_update_fan(config, delta);

    delay(CTRL_DELAY_TIME);
    fflush(stdout);
  }

  printf("ctrl :: stopped\n");
}
