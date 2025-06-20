#!/bin/sh

picom --config ~/.config/picom/picom.conf &
xrandr --output Virtual-1 --mode 1366x768
randomWall.sh &
# xwallpaper --zoom /home/abir101/.local/share/backgrounds/wall2.png
~/.config/dmenu_scripts/cliphistd.sh &
export XCURSOR_THEME=macOS
export XCURSOR_SIZE=23
export XDG_RUNTIME_DIR=/tmp/$USER-runtime
pipewire &
wireplumber &

exec qtile start
# exec sxwm
