#!/bin/bash

# Start PipeWire if not already running
if ! pgrep -x pipewire >/dev/null; then
    pipewire &
fi

# Wait a bit for PipeWire to initialize
sleep 1

# Start WirePlumber if not already running
if ! pgrep -x wireplumber >/dev/null; then
    wireplumber &
fi
