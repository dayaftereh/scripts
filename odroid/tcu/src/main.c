#include <stdio.h>
#include <signal.h>

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
  printf( "stopping controller...\n");
}

void add_fan_runtime(){
  FAN_TIMER += 10000;
  printf( "adding fan runtime...\n");
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
    printf( "fail to read configuration from [ %s ]\n", params.config_file);
    return 2;
  }

  // ------------------------------------------------

  if(pid_write_file(params.pid_file) != PID_OK){
    printf( "fail to write pidfile to [ %s ]\n", params.pid_file);
  }

  // ------------------------------------------------

  if(params.verbose){
    printf("%s\n", proc_name);
    printf( "fan pin: [ %d ]\n", config.fan_pin );
    printf( "fan runtime: [ %d ms ]\n", config.fan_runtime );
    printf( "dht22 threshold: [ %f C ]\n", config.dht22_threshold );
    printf( "tmu threshold: [ %f C ]\n", config.tmu_threshold );
    printf( "dht22 pin: [ %d ]\n", config.dht22_pin );
    printf( "gpio mode: [ %d ]\n", config.gpio_mode );
    printf( "version: [ %s ]\n", version );
    printf( "pidfile: [ %s ]\n", params.pid_file );
    printf( "configfile: [ %s ]\n", params.config_file );
    printf( "tmufile: [ %s ]\n", config.tmu_file );
  }

  // ------------------------------------------------

  gpio_initialize(&config);

  // ------------------------------------------------

  signal(SIGINT, signal_handler);
  signal(SIGUSR1, signal_handler);
  signal(SIGTERM, signal_handler);

  // ------------------------------------------------

  RUNNING = 1;
  ctrl_run(&config, params.verbose);

  // ------------------------------------------------

  printf( "good bye\n");

  return 0;
}
