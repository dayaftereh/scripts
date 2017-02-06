#ifndef TMU_H
#define TMU_H

// -----------------------------------------------

#include <stdio.h>
#include <string.h>

#include "include/config.h"

// -----------------------------------------------

#define TMU_DELIM ":"
#define TMU_FACTOR 1000.0f
#define TMU_LINE_BUF_LEN 1024

// -----------------------------------------------

typedef enum {
  TMU_OK,
  TMU_ERROR,
} TMUErrorCode;

// -----------------------------------------------

TMUErrorCode tmu_read(struct Config *config, float *tmu);

// -----------------------------------------------

#endif /* TMU_H */
