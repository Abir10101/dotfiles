#!/bin/sh

picom --config ~/.config/picom/picom.conf &
randomWall.sh &
# xwallpaper --zoom /home/abir101/.local/share/backgrounds/wall2.png
~/.config/dmenu_scripts/cliphistd.sh &
export XCURSOR_THEME=macOS
export XCURSOR_SIZE=23
startaudio.sh &

exec qtile start
# exec sxwm
