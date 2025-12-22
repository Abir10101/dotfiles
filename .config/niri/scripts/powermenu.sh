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

case "$(printf "zzz\nreboot\nshutdown" | bemenu -i -p 'Power menu:' --fn 'Overpass Bold 11' -H 21 --hp 10 "${BEMENU_MATUGEN_COLORS[@]}")" in
	zzz) swaylock -f && sudo zzz ;;
	reboot) sudo reboot ;;
	shutdown) sudo poweroff ;;
	*) exit 1 ;;
esac
