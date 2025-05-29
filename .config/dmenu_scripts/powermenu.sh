#!/usr/bin/env bash

case "$(printf "zzz\nreboot\nshutdown" | dmenu -i -l 3 -p 'Power menu:')" in
	zzz) slock systemctl suspend -i ;;
	reboot) systemctl reboot -i ;;
	shutdown) shutdown now ;;
	*) exit 1 ;;
esac
