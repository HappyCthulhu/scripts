#!/bin/bash

fifo="/tmp/rofi_fifo"
kanshi_config="$HOME/.config/kanshi/config"

# Функция для отображения справки
function show_help {
    echo "Использование: $0 [опции]"
    echo
    echo "Опции:"
    echo "  -d, --daemon        Запуск в режиме демона, создающего файл FIFO"
    echo "  -s, --switch-to     Запуск rofi для выбора профиля и выполнения команд"
    echo "  -h, --help          Показать это сообщение и выйти"
}

# Функция для запуска демона
function run_daemon {
    # Чтение конфигурации kanshi и создание списка профилей
    layouts=()
    while IFS= read -r line; do
        if [[ $line == profile* ]]; then
            layout=$(echo "$line" | awk '{print $2}' | tr -d '"')
            layouts+=("$layout")
        fi
    done < "$kanshi_config"

    # Основной цикл демона
    while true; do
        {
            echo "enable output"
            for layout in "${layouts[@]}"; do
                echo "$layout"
            done
        } > "$fifo"
        sleep 1
    done
}

# Функция для выполнения команды по выбору пользователя
function switch_to {
    selected=$(cat "$fifo" | rofi -dmenu -p "Select Command")
    
    if [[ $selected == "enable output" ]]; then
        swaymsg "output * enable"
    else
        kanshictl switch "$selected"
    fi
}

# Основной обработчик аргументов
case "$1" in
    -d|--daemon)
        run_daemon
        ;;
    -s|--switch-to)
        switch_to
        ;;
    -h|--help)
        show_help
        ;;
    *)
        echo "Неизвестная опция: $1"
        show_help
        exit 1
        ;;
esac
