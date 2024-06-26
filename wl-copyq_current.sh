#!/usr/bin/env bash

# Попытаемся получить тип данных, хранящихся в буфере обмена
TYPE=$(wl-paste -t text --no-newline)

# Проверяем, есть ли текстовые данные
if [[ $TYPE ]]; then
  # Если тип данных - текст, копируем содержимое в переменную
  TEXT_IN_BUFFER=$(wl-paste --no-newline)
  # Проверяем длину текста и обрезаем, если необходимо
  if [ ${#TEXT_IN_BUFFER} -gt 1000 ]; then
    TEXT_IN_BUFFER="${TEXT_IN_BUFFER:0:1000}..." # Добавляем многоточие в конец, чтобы указать на обрезку
  fi
  echo "$TEXT_IN_BUFFER"
  notify-send -t 1000 -r 1 "$TEXT_IN_BUFFER"
else
  # Если в буфере не текст, предполагаем, что это изображение и сохраняем его
  TEMP_FILE=$(mktemp --suffix=.png)
  wl-paste > "$TEMP_FILE"
  notify-send -t 1000 -i "$TEMP_FILE" -h int:clip_height:1000 "Image in clipboard"
fi
