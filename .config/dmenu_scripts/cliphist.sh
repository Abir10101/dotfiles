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
  [ -f "$histfile" ] || touch "$histfile"
  [ -z "$clip" ] && exit 0
  multiline=$(echo "$clip" | sed ':a;N;$!ba;s/\n/'"$placeholder"'/g')
  grep -Fxq "$multiline" "$histfile" || echo "$multiline" >> "$histfile"
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
