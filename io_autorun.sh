#!/bin/bash
# Nous Observatory — I/O auto-refresh runner
# Runs conference-update-insert.py and logs output with a timestamp.
# Called by cron 3x/day on Google I/O dates.

REPO="/Users/itsvike/Documents/Claude/Projects/nous-observatory"
LOG="$REPO/logs/io_autorun.log"

mkdir -p "$REPO/logs"
echo "──────────────────────────────────────────" >> "$LOG"
echo "Run: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG"
python3 "$REPO/conference-update-insert.py" >> "$LOG" 2>&1
echo "Exit: $?" >> "$LOG"
