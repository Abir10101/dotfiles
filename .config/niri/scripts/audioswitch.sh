#!/bin/bash

NB="#19120c"
NF="#d6c3b6"
SB="#6b3b05"
SF="#ffdcc1"
TB="$NB"
TF="$NF"
HB="$SB"
HF="$SF"
AF="$NF"
AB="$NB"

BEMENU_MATUGEN_COLORS=(
  --nb "$NB" --nf "$NF"
  --sb "$SB" --sf "$SF"
  --ab "$AB" --af "$AF"
  --tb "$TB" --tf "$TF"
  --hb "$HB" --hf "$HF"
)

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
  choice=$(printf "Headphones\nSpeakers" | bemenu -i -p "Audio output:" --fn 'Overpass Bold 11' -H 21 --hp 10 "${BEMENU_MATUGEN_COLORS[@]}")
  case "$choice" in
    Headphones) headphones;;
    Speakers) speakers;;
  esac
}
choosespeakers "$@"
