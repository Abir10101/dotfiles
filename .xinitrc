#!/bin/sh

# comment for vm
picom --config ~/.config/picom/picom.conf &

# uncomment for vm
# xrandr --output Virtual-1 --mode 1366x768

randomWall.sh &
~/.config/dmenu_scripts/cliphistd.sh &
export XCURSOR_THEME=macOS
export XCURSOR_SIZE=23
startaudio.sh &

exec qtile start
