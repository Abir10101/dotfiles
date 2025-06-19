#!/usr/bin/env bash
# Set audio sinks before using!
# `pactl list sinks` if on pulseaudio.

# headphones () { \
#   pactl set-default-sink "alsa_output.usb-TTGK_Technology_Co._Ltd_Headphone_Zone_x_ddHiFi_DAC-00.iec958-stereo" &
# }

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
  # wpctl set-default 56
}

choosespeakers() { \
  choice=$(printf "Headphones\\nSpeakers" | dmenu -l 2 -i -p "Audio output:")
  case "$choice" in
    Headphones) headphones;;
    Speakers) speakers;;
  esac
}

choosespeakers
