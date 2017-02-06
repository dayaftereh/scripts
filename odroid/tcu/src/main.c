#include <stdio.h>
#include <signal.h>

#include "include/dht22.h"

#include "include/pid.h"
#include "include/gpio.h"
#include "include/ctrl.h"
#include "include/config.h"
#include "include/params.h"

// ----------------------------------------------------------------------------

volatile sig_atomic_t RUNNING;
volatile sig_atomic_t FAN_TIMER;

// ----------------------------------------------------------------------------

void stop_ctrl(){
  RUNNING = 0;
  printf( "main :: stopping controller...\n");
}

void add_fan_runtime(){
  FAN_TIMER += 10000;
  printf( "main :: adding fan runtime...\n");
}

// ----------------------------------------------------------------------------

void signal_handler(int signum)
{
  switch(signum){
    case SIGINT:
      stop_ctrl();
      break;
    case SIGTERM:
      stop_ctrl();
      break;
    case SIGUSR1:
      add_fan_runtime();
      break;
  }
}

// ----------------------------------------------------------------------------

int main(int argc, char* argv[])
{
  // ------------------------------------------------
  struct Params params;
  if(params_read(&params, argc, argv) == PARAMS_HELP){
    params_help();
    return 0;
  }

  if(params_check(&params) != PARAMS_OK){
    params_help();
    return 1;
  }

  // ------------------------------------------------

  struct Config config;
  if(config_read(params.config_file, &config) != CONFIG_OK){
    printf( "conf :: can't read configuration from file [ %s ]\n", params.config_file);
    return 2;
  }

  // ------------------------------------------------

  if(pid_write_file(params.pid_file) != PID_OK){
    printf( "pid :: can't write pidfile to [ %s ]\n", params.pid_file);
  }

  // ------------------------------------------------

  if(params.verbose){
    printf("info :: %s\n", proc_name);
    printf("info :: fan pin: [ %d ]\n", config.fan_pin );
    printf("info :: fan runtime: [ %.3f s ]\n", (config.fan_runtime / 1000.0f) );
    printf("info :: dht22 threshold: [ %.1f C ]\n", config.dht22_threshold );
    printf("info :: tmu threshold: [ %.1f C ]\n", config.tmu_threshold );
    printf("info :: dht22 pin: [ %d ]\n", config.dht22_pin );
    printf("info :: gpio mode: [ %d ]\n", config.gpio_mode );
    printf("info :: version: [ %s ]\n", version );
    printf("info :: pidfile: [ %s ]\n", params.pid_file );
    printf("info :: configfile: [ %s ]\n", params.config_file );
    printf("info :: tmufile: [ %s ]\n", config.tmu_file );
  }

  // ------------------------------------------------

  gpio_initialize(&config);

  // ------------------------------------------------

  if(dht22_check_pull_up(&config) != DHT22_OK){
    printf( "dht22 :: missing a pull up resistor on data line,\n");
    return 3;
  }

  // ------------------------------------------------

  signal(SIGINT, signal_handler);
  signal(SIGUSR1, signal_handler);
  signal(SIGTERM, signal_handler);

  // ------------------------------------------------

  RUNNING = 1;
  ctrl_run(&config, params.verbose);

  // ------------------------------------------------

  printf( "main :: good bye\n");

  return 0;
}
