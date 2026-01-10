#!/usr/bin/env bash

if pgrep -x hypridle >/dev/null 2>&1; then
    echo "💤"
else
    echo "🔓"
fi

