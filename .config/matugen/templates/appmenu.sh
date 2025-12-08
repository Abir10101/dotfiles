#!/bin/bash

NB="{{colors.background.default.hex}}"
NF="{{colors.on_surface_variant.default.hex}}"
SB="{{colors.primary_container.default.hex}}"
SF="{{colors.on_primary_container.default.hex}}"
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
