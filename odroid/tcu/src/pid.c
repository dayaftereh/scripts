#include "include/pid.h"

// ----------------------------------------------------------------------------

PIDErrorCode pid_write_file(const char *file){
  FILE *fp = fopen(file, "w");

  if(fp == NULL){
    return PID_ERROR;
  }

  pid_t pid = getpid();
  if (fprintf(fp, "%ld", (long)pid) == -1){
    fclose(fp);
    return PID_ERROR;
  }

  fclose(fp);
  return PID_OK;
}
