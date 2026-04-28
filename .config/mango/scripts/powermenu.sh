#!/bin/bash

NB="#14140c"
NF="#cac7b6"
SB="#4b4900"
SF="#eae68e"
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
