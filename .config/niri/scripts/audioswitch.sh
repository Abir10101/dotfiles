#!/bin/bash

headphones () { \
  SINK_NAME="Headphone Zone x ddHiFi DAC Digital Stereo"
  SINK_ID=$(wpctl status | awk -v name="$SINK_NAME" -F '[.()]' '$0 ~ name {print $1}' | awk '{print $NF}')
  if [ -n "$SINK_ID" ]; then
      wpctl set-default "$SINK_ID"
  fi
}
speakers () { \
  SINK_NAME="Built-in Audio Analog Stereo"
  SINK_ID=$(wpctl status | awk -v name="$SINK_NAME" -F '[.()]' '$0 ~ name {print $1}' | awk '{print $NF}')
  if [ -n "$SINK_ID" ]; then
      wpctl set-default "$SINK_ID"
  fi
}
choosespeakers() { \
  choice=$(printf "Headphones\\nSpeakers" | bemenu -i -p "Audio output:" "$@")
  case "$choice" in
    Headphones) headphones;;
    Speakers) speakers;;
  esac
}
choosespeakers "$@"
