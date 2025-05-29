#!/usr/bin/env bash
# Set audio sinks before using!
# `pactl list sinks` if on pulseaudio.

headphones () { \
  pacmd set-default-sink "alsa_output.usb-TTGK_Technology_Co._Ltd_Headphone_Zone_x_ddHiFi_DAC-00.iec958-stereo" &
}

speakers () { \
  pacmd set-default-sink "alsa_output.pci-0000_00_1f.3.analog-stereo" &
}

choosespeakers() { \
  choice=$(printf "Headphones\\nSpeakers" | dmenu -l 2 -i -p "Audio output:")
  case "$choice" in
    Headphones) headphones;;
    Speakers) speakers;;
  esac
}

choosespeakers
