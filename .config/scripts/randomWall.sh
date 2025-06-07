#!/bin/bash

# Directory containing your wallpapers
WALLPAPER_DIR="$HOME/.local/share/backgrounds/"

# Pick a random image file
IMAGE=$(find "$WALLPAPER_DIR" -type f \( -iname '*.jpg' -o -iname '*.png' \) | shuf -n 1)

# Set wallpaper using xwallpaper (fill mode)
xwallpaper --zoom "$IMAGE"
