#!/bin/bash

NB="#121318"
NF="#c7c5d0"
SB="#3a4379"
SF="#dee0ff"
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
