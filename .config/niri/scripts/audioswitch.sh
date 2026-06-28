#!/bin/bash

NB="#0f1512"
NF="#bfc9c3"
SB="#005140"
SF="#a2f2d8"
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
  choice=$(printf "Headphones\nSpeakers" | bemenu -i -p "Audio output:" --fn 'Inter Display Bold 10' -H 24 --hp 10 "${BEMENU_MATUGEN_COLORS[@]}")
  case "$choice" in
    Headphones) headphones;;
    Speakers) speakers;;
  esac
}
choosespeakers "$@"
