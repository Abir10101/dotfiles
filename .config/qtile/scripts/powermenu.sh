#!/bin/bash

case "$(printf "zzz\nreboot\nshutdown" | bemenu -i -p 'Power menu:' "$@")" in
	zzz) sudo zzz && slock;;
	reboot) sudo reboot ;;
	shutdown) sudo poweroff ;;
	*) exit 1 ;;
esac
