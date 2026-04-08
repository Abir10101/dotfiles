#!/bin/bash

NB="#101417"
NF="#c1c7ce"
SB="#004c6d"
SF="#c8e6ff"
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

bemenu-run --fn 'Overpass Bold 11' -H 21 --hp 6 -p menu "${BEMENU_MATUGEN_COLORS[@]}"
