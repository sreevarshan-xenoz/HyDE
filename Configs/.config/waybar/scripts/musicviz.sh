#!/bin/bash
# Reads cava output from FIFO and prints unicode bars

FIFO="/tmp/cava-waybar"
if [ ! -p "$FIFO" ]; then
  mkfifo "$FIFO"
fi

# Start cava if not running
if ! pgrep -x cava > /dev/null; then
  cava -p ~/.config/cava/config-waybar &>/dev/null &
fi

# Read and print bars
read -t 0.1 bars < "$FIFO"
if [ -n "$bars" ]; then
  # Convert numbers to unicode blocks (▁▂▃▄▅▆▇█)
  out=""
  for n in $bars; do
    case $n in
      0) out+="▁";;
      1) out+="▂";;
      2) out+="▃";;
      3) out+="▄";;
      4) out+="▅";;
      5) out+="▆";;
      6) out+="▇";;
      7) out+="█";;
      *) out+=" ";;
    esac
  done
  echo "$out"
else
  echo " "
fi 