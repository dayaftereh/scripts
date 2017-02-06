#include "include/ctrl.h"

// ----------------------------------------------------------------------------

void ctrl_update_tmu(struct Config *config){
  float tmu;
  if(tmu_read(config, &tmu) != TMU_OK){
    printf( "fail to read tmu\n");
    return;
  }

  if(tmu > config->tmu_threshold && FAN_TIMER <= 0){
    FAN_TIMER = config->fan_runtime;
    printf( "tmu reached threshold [ %f > %f ]\n", tmu, config->tmu_threshold);
  }
}

void ctrl_update_dht22(struct Config *config){
  float humidity;
  float temperature;

  if(dht22_read(config->dht22_pin, &humidity, &temperature) != DHT_OK){
    printf( "fail to read dht22\n");
    return;
  }

  if(temperature > config->dht22_threshold && FAN_TIMER <= 0){
    FAN_TIMER = config->fan_runtime;
    printf( "dht22 reached threshold [ %f > %f ]\n", temperature, config->dht22_threshold);
  }
}

// ----------------------------------------------------------------------------

void ctrl_update_fan(struct Config *config, int delta) {
  if(FAN_TIMER <= 0){
    return;
  }

  fan_start(config);
  FAN_TIMER -= delta;

  if(FAN_TIMER <= 0) {
    fan_stop(config);
    printf( "stopping fan, becuase runtime reached\n");
  }
}

// ----------------------------------------------------------------------------

int ctrl_calc_delta(int *last_update){
  int delta = millis() - *last_update;
  *last_update = millis();
  return delta;
}

// ----------------------------------------------------------------------------

void ctrl_run(struct Config *config, int verbose){
  int last_update = millis();
  FAN_TIMER = config->fan_runtime;
  
  while(RUNNING){
    ctrl_update_tmu(config);
    ctrl_update_dht22(config);

    int delta = ctrl_calc_delta(&last_update);
    ctrl_update_fan(config, delta);

    delay(CTRL_DELAY_TIME);
  }
}