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

case "$(printf "zzz\nreboot\nshutdown" | bemenu -i -p 'Power menu:' --fn 'Inter Display Bold 10' -H 24 --hp 10 "${BEMENU_MATUGEN_COLORS[@]}")" in
	zzz) swaylock -f && sudo zzz ;;
	reboot) sudo reboot ;;
	shutdown) sudo poweroff ;;
	*) exit 1 ;;
esac
