#!/usr/bin/bash
AVAILABLE_ARGS=("next" "previous")

DIRECTION=$1

if ! [[ " ${AVAILABLE_ARGS[*]} " =~ " $DIRECTION " ]]; then
    echo "Wrong arg"
    exit 1
fi

# Мы устанавливаем ID каждого уведомления равным 1
# Если уведомление с ID 1 уже существует - новое уведомление его заменит
# Если нет - появится новое уведомление
NOTIF_ID=1

copyq $DIRECTION
TYPE="$(wl-paste --type text/plain --list-types)"

# Проверяем тип данных в буфере обмена
if [[ $TYPE == *"image/png"* ]]; then
  # Если тип данных - изображение
  TEMP_FILE=$(mktemp --suffix=.png)
  wl-paste --type image/png > "$TEMP_FILE"
  notify-send -t 1000 -r $NOTIF_ID -i $TEMP_FILE -h int:clip_height:1000 pic clip
#  feh --bg-scale $TEMP_FILE
else
  TEXT="$(wl-paste --type text/plain)"
  # Проверяем длину текста и обрезаем, если необходимо
  if [ ${#TEXT} -gt 1000 ]; then
    TEXT="${TEXT:0:1000}..." # Добавляем многоточие в конец, чтобы указать на обрезку
  fi
  notify-send -t 1000 -r $NOTIF_ID "$TEXT"
fi
