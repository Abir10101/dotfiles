#!/bin/bash

NB="#1a110f"
NF="#d8c2bc"
SB="#723523"
SF="#ffdbd1"
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
