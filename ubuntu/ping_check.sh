#!/bin/bash

COMMAND="$1"
TIMEOUT="15"
WAIT_TIMEOUT="30"
ADDRESS="8.8.8.8"

while true; do
  timeout $TIMEOUT ping -c 1 $ADDRESS
  if [ "$?" != "0" ]; then
    ###################################################
    echo "ping failed, executing now given commands..."
    for COMMAND in "$@"; do
      echo "run $COMMAND"
      eval "$COMMAND"
    done
    ###################################################
    echo "waiting now [ $WAIT_TIMEOUT ] seconds"
    sleep $WAIT_TIMEOUT
  fi
  sleep 10
done
