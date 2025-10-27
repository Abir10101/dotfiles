#!/bin/bash

cliphist list | bemenu -l 5 -i -p 'Clipboard:' "$@" | cliphist decode | wl-copy
