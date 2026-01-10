#!/usr/bin/env bash

if pgrep -x hypridle >/dev/null 2>&1; then
    pkill hypridle >/dev/null 2>&1
    notify-send "Hypridle" "Auto lock & suspend DISABLED"
else
    hypridle >/dev/null 2>&1 &
    notify-send "Hypridle" "Auto lock & suspend ENABLED"
fi

