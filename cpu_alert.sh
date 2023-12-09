#!/bin/bash
# This script monitors memory usage and sends a notification if it exceeds 95%

# Threshold for memory usage
THRESHOLD=95

while :
do 
  # Get the current usage of memory
  memUsage=$(free -m | awk '/Mem:/{print $3/$2 * 100.0}')
  
  # Check if memory usage exceeds the threshold
  if (( $(echo "$memUsage > $THRESHOLD" | bc -l) )); then
    notify-send "High Memory Usage" "Your memory usage is at ${memUsage}%!"
  fi

  # Sleep for some time
  sleep 1
done

