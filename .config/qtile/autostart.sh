#!/bin/bash

# while pgrep -u $UID -x picom >/dev/null; do sleep 1; done
# picom --config ~/.config/picom/picom.conf &
# xfce4-clipman &
# Start picom if it's not already running
if ! pgrep -u "$UID" -x picom >/dev/null; then
    picom --config ~/.config/picom/picom.conf &
fi

# Start Clipman if not already running
if ! pgrep -u "$UID" -x xfce4-clipman >/dev/null; then
    xfce4-clipman &
fi
