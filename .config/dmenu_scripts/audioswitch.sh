#!/usr/bin/env bash
# Set audio sinks before using!
# `pactl list sinks` if on pulseaudio.

# headphones () { \
#   pactl set-default-sink "alsa_output.usb-TTGK_Technology_Co._Ltd_Headphone_Zone_x_ddHiFi_DAC-00.iec958-stereo" &
# }

headphones () { \
  wpctl set-default 57
}

speakers () { \
  wpctl set-default 45
}

choosespeakers() { \
  choice=$(printf "Headphones\\nSpeakers" | dmenu -l 2 -i -p "Audio output:")
  case "$choice" in
    Headphones) headphones;;
    Speakers) speakers;;
  esac
}

choosespeakers
