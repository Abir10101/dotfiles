#!/bin/sh

export XDG_SESSION_TYPE=wayland
export QT_QPA_PLATFORM=wayland
export XDG_CURRENT_DESKTOP=wlroots

# xwayland-satellite

# randomWall.sh &
wl-paste --type text --watch cliphist store &
$HOME/.local/bin/startaudio.sh
