#!/bin/sh

# Load X resources
# xrdb -merge ~/.Xresources

nm-applet &
picom --config ~/.config/picom/picom.conf &
xfce4-clipman &

# Start Qtile
exec qtile start
