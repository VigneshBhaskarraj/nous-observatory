#!/bin/bash
# Installs cron entries to auto-run conference-update-insert.py
# 3x/day on Google I/O 2026 (May 19–20).
#
# Times (PDT = UTC-7):
#   11:00 AM PDT = 18:00 UTC  — after keynote starts
#    2:00 PM PDT = 21:00 UTC  — after dev keynote
#    7:00 PM PDT = 02:00 UTC  — end-of-day wrap
#
# Usage: bash install_io_cron.sh

SCRIPT_PATH="/Users/itsvike/Documents/Claude/Projects/nous-observatory/io_autorun.sh"

# Marker so we can cleanly remove just our entries later
MARKER="# nous-observatory-io26"

# Build the 6 cron lines (3 times × 2 days)
NEW_ENTRIES=$(cat <<CRON
$MARKER
0 18 19 5 * $SCRIPT_PATH $MARKER
0 21 19 5 * $SCRIPT_PATH $MARKER
0 2  20 5 * $SCRIPT_PATH $MARKER
0 18 20 5 * $SCRIPT_PATH $MARKER
0 21 20 5 * $SCRIPT_PATH $MARKER
0 2  21 5 * $SCRIPT_PATH $MARKER
CRON
)

# Check not already installed
if crontab -l 2>/dev/null | grep -q "nous-observatory-io26"; then
  echo "⚠  Cron entries already installed. Run remove_io_cron.sh first if you want to reinstall."
  exit 0
fi

# Append to existing crontab (or create new one)
(crontab -l 2>/dev/null; echo "$NEW_ENTRIES") | crontab -

echo "✓ Installed 6 cron entries for Google I/O 2026 (May 19–20)."
echo ""
echo "Schedule (all times PT / PDT):"
echo "  May 19  11:00 AM, 2:00 PM, 7:00 PM"
echo "  May 20  11:00 AM, 2:00 PM, 7:00 PM"
echo ""
echo "Logs will appear in:"
echo "  /Users/itsvike/Documents/Claude/Projects/nous-observatory/logs/io_autorun.log"
echo ""
echo "To remove after the conference: bash remove_io_cron.sh"
