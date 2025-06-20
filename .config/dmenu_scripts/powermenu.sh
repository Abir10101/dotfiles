#!/usr/bin/env bash

case "$(printf "zzz\nreboot\nshutdown" | dmenu -i -l 3 -p 'Power menu:')" in
	zzz) slock && sudo zzz ;;
	reboot) sudo reboot ;;
	shutdown) sudo poweroff ;;
	*) exit 1 ;;
esac
