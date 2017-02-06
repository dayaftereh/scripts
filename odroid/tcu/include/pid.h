#ifndef PID_H
#define PID_H

// -----------------------------------------------

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

// -----------------------------------------------

typedef enum {
  PID_OK,
  PID_ERROR,
} PIDErrorCode;

// -----------------------------------------------

PIDErrorCode pid_write_file(const char *file);

// -----------------------------------------------

#endif /* PID_H */
