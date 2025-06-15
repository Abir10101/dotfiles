#!/usr/bin/env bash

# last=""
# cliphist_path="$HOME/.config/dmenu_scripts/cliphist.sh"

# while true; do
#   clip="$(xsel -o -b)"
#   if [ -n "$clip" ]; then
#     printf "%s" "$clip" | "$cliphist_path" out
#     last="$clip"
#   fi
#   sleep 1
# done

#!/usr/bin/env bash

last=""
cliphist_path="$HOME/.config/dmenu_scripts/cliphist.sh"

while clipnotify; do
  clip="$(xsel -o -b)"
  if [ -n "$clip" ] && [ "$clip" != "$last" ]; then
    printf "%s" "$clip" | "$cliphist_path" out
    last="$clip"
  fi
done
