#include "include/tmu.h"

// ----------------------------------------------------------------------------

TMUErrorCode tmu_read(struct Config *config, float *tmu){

  FILE *fp = fopen(config->tmu_file, "r");
  if(fp == NULL){
    return TMU_ERROR;
  }

  int sum = 0;
  int count = 0;
  char line[TMU_LINE_BUF_LEN];
  
  while(fgets(line, TMU_LINE_BUF_LEN, fp)) {
    char *cfline = strstr((char *)line, TMU_DELIM);
    if(cfline != NULL){
      char *value_ptr = cfline + strlen(TMU_DELIM);
      int tmu = atoi(value_ptr);
      sum += tmu;
      count++;
    }
  }

  *tmu = (sum / ((float) count)) / TMU_FACTOR;
  return TMU_OK;
}
