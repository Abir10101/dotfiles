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

cliphist list | bemenu -l 5 -i -p 'Clipboard:' --fn 'Overpass Bold 10' -H 21 "${BEMENU_MATUGEN_COLORS[@]}" | cliphist decode | wl-copy
