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
    echo "  -c, --config NAME   Переключение на указанный профиль NAME"
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

# Функция для установки указанного профиля
function set_layout {
    local layout_name="$1"

    # Проверка, существует ли профиль в конфигурации kanshi
    if grep -q "profile \"$layout_name\"" "$kanshi_config"; then
        kanshictl switch "$layout_name"
        echo "Переключение на профиль: $layout_name"
    else
        echo "Ошибка: Профиль \"$layout_name\" не найден в $kanshi_config"
        exit 1
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
    -c|--config)
        if [[ -z "$2" ]]; then
            echo "Ошибка: Не указан профиль для переключения."
            exit 1
        fi
        set_layout "$2"
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
