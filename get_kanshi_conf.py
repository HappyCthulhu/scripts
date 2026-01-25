#!/usr/bin/env python3
import json
import subprocess
import argparse

# map Hyprland transform -> kanshi rotate
# Hyprland transform (wl_output_transform): 0=normal,1=90,2=180,3=270,4=flipped,5=flipped-90,6=flipped-180,7=flipped-270
KANSHI_ROTATE = {
    0: None,
    1: "90",
    2: "180",
    3: "270",
    # flipped варианты kanshi поддерживает как rotate? — обычно используют transform.
    # Укажем transform напрямую, если flipped.
    4: "flipped",
    5: "flipped-90",
    6: "flipped-180",
    7: "flipped-270",
}

def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return p.stdout

def load_monitors():
    data = run(["hyprctl", "-j", "monitors"])
    mons = json.loads(data)
    # hyprctl -j monitors возвращает список словарей
    return [m for m in mons if m.get("active", True)]

def gen_kanshi(monitors):
    # Пример строки в kanshi:
    #   output "DP-1" mode 2560x1440@144 position 0,0 scale 1.25
    #   + при необходимости transform/rotate
    lines = ['profile "new_config" {']
    for m in monitors:
        name = m["name"]
        w = m["width"]
        h = m["height"]
        rr = int(round(m.get("refreshRate") or m.get("refresh", 60)))
        x = m.get("x", 0)
        y = m.get("y", 0)
        scale = m.get("scale", 1)
        transform = int(m.get("transform", 0))

        line = f'    output "{name}" mode {w}x{h}@{rr} position {x},{y} scale {scale}'
        rot = KANSHI_ROTATE.get(transform)
        if rot:
            # Для flipped-*, kanshi также понимает transform <value>.
            if rot.startswith("flipped"):
                line += f" transform {rot}"
            else:
                line += f" rotate {rot}"
        lines.append(line)
    lines.append("}")
    return "\n".join(lines)

def gen_hypr(monitors):
    # Формат Hyprland:
    #   monitor=<name>,<WxH>@<RR>,<X>x<Y>,<scale>[,<transform>]
    # Пример:
    #   monitor=DP-1,2560x1440@144,0x0,1.25
    # transform можно опустить, если normal (0)
    lines = []
    for m in monitors:
        name = m["name"]
        w = m["width"]
        h = m["height"]
        rr = int(round(m.get("refreshRate") or m.get("refresh", 60)))
        x = m.get("x", 0)
        y = m.get("y", 0)
        scale = m.get("scale", 1)
        transform = int(m.get("transform", 0))

        base = f"monitor={name},{w}x{h}@{rr},{x}x{y},{scale}"
        if transform != 0:
            # В Hyprland transform — целое число (0..7), можно добавить пятым аргументом
            base += f",{transform}"
        lines.append(base)
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Generate kanshi or Hyprland monitor config from current Hyprland state")
    ap.add_argument("--hypr", action="store_true", help="output Hyprland monitor= lines instead of kanshi profile")
    args = ap.parse_args()

    monitors = load_monitors()
    if args.hypr:
        print(gen_hypr(monitors))
    else:
        print(gen_kanshi(monitors))

if __name__ == "__main__":
    main()
