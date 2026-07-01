#!/bin/bash
# Уведомляет о низком заряде батареи на порогах 15, 10, 5 и 2 %.

THRESHOLDS=(15 10 5 2)
POLL_INTERVAL=10

get_battery_info() {
    local ps capacity status

    for ps in /sys/class/power_supply/BAT*; do
        [[ -d "$ps" ]] || continue
        [[ "$(cat "$ps/type" 2>/dev/null)" == "Battery" ]] || continue

        capacity=$(cat "$ps/capacity" 2>/dev/null) || continue
        status=$(cat "$ps/status" 2>/dev/null)

        echo "$capacity $status"
        return 0
    done

    return 1
}

is_discharging() {
    [[ "$1" == "Discharging" || "$1" == "Not charging" ]]
}

notify_threshold() {
    local level=$1
    local capacity=$2

    notify-send -u critical "Низкий заряд батареи" \
        "Заряд батареи достиг ${level}% (сейчас ${capacity}%)"
}

prev_capacity=""
first_read=true

while :; do
    if read -r capacity status <<< "$(get_battery_info)"; then
        if is_discharging "$status"; then
            if [[ "$first_read" == true ]]; then
                prev_capacity=$capacity
                first_read=false
            else
                for level in "${THRESHOLDS[@]}"; do
                    if (( prev_capacity > level && capacity <= level )); then
                        notify_threshold "$level" "$capacity"
                    fi
                done
                prev_capacity=$capacity
            fi
        else
            prev_capacity=$capacity
            first_read=false
        fi
    fi

    sleep "$POLL_INTERVAL"
done
