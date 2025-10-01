#!/usr/bin/env bash

histfile="$HOME/.cache/cliphist"
placeholder="<NEWLINE>"

highlight() {
  clip=$(xsel -o -p)
  echo -n "$clip" | xsel -i -b
}

output() {
  clip=$(cat)
  echo -n "$clip" | xsel -i -b
}

write() {
  # [ -f "$histfile" ] || touch "$histfile"
  # [ -z "$clip" ] && exit 0
  # multiline=$(echo "$clip" | sed ':a;N;$!ba;s/\n/'"$placeholder"'/g')
  # tail -n 5 "$histfile" | grep -Fxq "$multiline" || echo "$multiline" >> "$histfile"

  # Exit early if $clip is empty
  [[ -z "$clip" ]] && exit 0

  # Ensure $histfile exists (only if it doesn't)
  [[ ! -f "$histfile" ]] && touch "$histfile"

  # Convert multiline clip to single line with placeholder
  multiline="${clip//$'\n'/$placeholder}"

  # Use awk for more efficient processing - removes matching lines and appends new one
  awk -v line="$multiline" '
      $0 != line { print }
      END { print line }
  ' "$histfile" > "${histfile}.tmp" && mv "${histfile}.tmp" "$histfile"
}

sel() {
  selection=$(tac "$histfile" | dmenu -l 5 -i -p "Clipboard history:")
  [ -n "$selection" ] && echo "$selection" | sed "s/$placeholder/\n/g" | xsel -i -b
}

case "$1" in
  add) highlight && write ;;
  out) output && write ;;
  sel) sel ;;
  *) printf "$0 | File: $histfile\n\nadd - copies primary selection to clipboard, and adds to history file\nout - pipe commands to copy output to clipboard, and add to history file\nsel - select from history file with dmenu and recopy!\n" ; exit 0 ;;
esac
