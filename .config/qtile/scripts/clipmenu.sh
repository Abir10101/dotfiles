#!/bin/bash

cliphist list | bemenu -l 5 -i -p 'Clipboard history:' "$@" | cliphist decode | wl-copy
