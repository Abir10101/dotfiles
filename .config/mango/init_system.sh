#!/bin/sh

export XDG_SESSION_TYPE=wayland
export QT_QPA_PLATFORM=wayland
export XDG_CURRENT_DESKTOP=mango

swaybg -o DP-1 -i /home/abir101/.local/share/backgrounds/wall18.jpg -m fill &
wl-paste --type text --watch cliphist store &
$HOME/.local/bin/startaudio.sh

waybar &
