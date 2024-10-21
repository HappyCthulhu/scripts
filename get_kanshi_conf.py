#!/bin/python
import json
import subprocess

# Получаем вывод swaymsg
output = subprocess.run(['swaymsg', '-t', 'get_outputs'], capture_output=True, text=True)
outputs = json.loads(output.stdout)

# Генерация kanshi config
config = "profile \"new_config\" {\n"
for display in outputs:
    if display["active"]:
        name = display["name"]
        width = display["current_mode"]["width"]
        height = display["current_mode"]["height"]
        refresh_rate = display["current_mode"]["refresh"]
        scale = display["scale"]
        pos_x = display["rect"]["x"]
        pos_y = display["rect"]["y"]
        config += f'    output "{name}" mode {width}x{height}@{int(refresh_rate)}Hz position {pos_x},{pos_y} scale {scale}\n'
config += "}"

# Сохраняем в файл
print(config)
