#!/bin/sh

# Load X resources
# xrdb -merge ~/.Xresources

nm-applet &
picom --config ~/.config/picom/picom.conf &
# xfce4-clipman &
~/.config/dmenu_scripts/cliphistd.sh &
export XCURSOR_THEME=macOS
export XCURSOR_SIZE=23

# Start Qtile
exec qtile start
# exec /usr/local/bin/startdwm.sh
