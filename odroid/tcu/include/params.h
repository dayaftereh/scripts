#ifndef PARAMS_H
#define PARAMS_H

// -----------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <limits.h>
#include <string.h>

// -----------------------------------------------

struct Params {
  int verbose;
  char *pid_file;
  char *config_file;
};

// -----------------------------------------------

typedef enum {
  PARAMS_OK,
  PARAMS_HELP,
  PARAMS_ERROR
} ParamsError;

// -----------------------------------------------

void params_help();
void params_init(struct Params *params);
ParamsError params_check(struct Params *params);
ParamsError params_read(struct Params *params, int argc, char* argv[]);

// -----------------------------------------------

#endif /* PARAMS_H */
