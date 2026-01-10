#!/usr/bin/env bash
set -euo pipefail

FIFO="/tmp/kanshi_rofi.fifo"
KONFIG="$HOME/.config/kanshi/config"
SLEEP_SEC=2

# -----------------------------
# HELP
# -----------------------------
show_help() {
    cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -d, --daemon        Start daemon (keeps FIFO updated)
  -s, --switch        Open rofi menu (client)
  -c, --config NAME   Switch directly to kanshi profile NAME
  -h, --help          Show this help and exit
EOF
}

# -----------------------------
# VALIDATION
# -----------------------------
[[ -f "$KONFIG" ]] || { echo "kanshi config not found: $KONFIG" >&2; exit 1; }

# -----------------------------
# GET LAYOUTS (no cache)
# -----------------------------
read_layouts() {
    grep -E '^profile "' "$KONFIG" | awk '{print $2}' | tr -d '"'
}

# -----------------------------
# DAEMON
# -----------------------------
run_daemon() {
    rm -f "$FIFO"
    mkfifo "$FIFO"

    trap 'rm -f "$FIFO"; exit 0' INT TERM EXIT

    while true; do
        {
            echo "🔆 dpms on"
            echo "🎬 dpms off"
            echo "🔄 reload kanshi"
            read_layouts
        } > "$FIFO"

        sleep "$SLEEP_SEC"
    done
}

# -----------------------------
# ACTIONS
# -----------------------------
do_dpms_on() {
    hyprctl dispatch dpms on
}

do_dpms_off() {
    hyprctl dispatch dpms off
}

reload_kanshi() {
    pkill kanshi || true
    kanshi &
}

switch_layout() {
    local name="$1"
    if ! grep -qE "^profile \"$name\"" "$KONFIG"; then
        echo "Profile '$name' not found" >&2
        exit 1
    fi
    kanshictl switch "$name"
}

# -----------------------------
# CLIENT (ROFI)
# -----------------------------
run_rofi() {
    local selected
    selected=$(cat "$FIFO" | rofi -dmenu -p "Display manager")

    [[ -z "$selected" ]] && exit 0

    case "$selected" in
        "🔆 dpms on")
            do_dpms_on
            ;;
        "🎬 dpms off")
            do_dpms_off
            ;;
        "🔄 reload kanshi")
            reload_kanshi
            ;;
        *)
            switch_layout "$selected"
            ;;
    esac
}

# -----------------------------
# CLI
# -----------------------------
case "${1:-}" in
    -d|--daemon)
        run_daemon
        ;;
    -s|--switch)
        run_rofi
        ;;
    -c|--config)
        [[ -n "${2:-}" ]] || { echo "Profile name required"; exit 1; }
        switch_layout "$2"
        ;;
    -h|--help)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
