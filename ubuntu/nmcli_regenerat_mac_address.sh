#!/bin/bash

CONNECTION="$1"
NEW_MAC_ADDRESS="$2"
PRE_MAC_ADDRESS="60:36:dd"

if [ -z "${CONNECTION}" ]; then
  echo "using active connection for changing mac address"
  CONNECTION=$(nmcli --terse --fields name connection show --active)
fi

if [ -z "${NEW_MAC_ADDRESS}" ]; then
  echo "generating new mac address..."
  HEXDUMP_OUTPUT=$(hexdump -n3 -e '/1 ":%02X"' /dev/random)
  NEW_MAC_ADDRESS="$PRE_MAC_ADDRESS$HEXDUMP_OUTPUT"
fi

echo "stopping connection [ $CONNECTION ].."
nmcli connection down "$CONNECTION"

echo "changing mac address for connection [ $CONNECTION ] to [ $NEW_MAC_ADDRESS ]"
nmcli connection modify --temporary "$CONNECTION" 802-11-wireless.cloned-mac-address $NEW_MAC_ADDRESS

echo "starting connection [ $CONNECTION ].."
nmcli connection up "$CONNECTION"
