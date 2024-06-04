window_exists=$(swaymsg -t get_tree | jq '[recurse(.nodes[]?, .floating_nodes[]?) | select(.name == "Telegram Web")] | length > 0')

if [ "$window_exists" = "false" ]; then
    google-chrome-stable --app=https://web.telegram.org/k/
fi

swaymsg [con_mark="tg"] scratchpad show
swaymsg [con_mark="tg"] resize set width 50ppt height 80ppt
swaymsg [con_mark="tg"] move position center center
