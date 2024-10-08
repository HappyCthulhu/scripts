#!/bin/bash

windows=$(xdotool search --onlyvisible --class "Google-chrome")
readarray -t windows_ids <<<"$windows"
window_count=${#windows_ids[@]}

google-chrome-stable --new-window "https://web.telegram.org/k/"

current_window_count=$window_count
while [ $current_window_count -eq $window_count ]; do

  current_windows=$(xdotool search --onlyvisible --class "Google-chrome")
  readarray -t current_windows_ids <<<"$current_windows"
  current_window_count=${#current_windows_ids[@]}

done


for id in "${current_windows_ids[@]}"; do

  if [[ ! " ${windows_ids[*]} " =~ ${id} ]]; then
    telegram_window_id=$id
  fi

done

while true; do

    wmctrl -i -r $telegram_window_id -N "tg_scratch"
    sleep 1

done
