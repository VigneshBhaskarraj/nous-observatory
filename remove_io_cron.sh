#!/bin/bash
# Removes the nous-observatory I/O 2026 cron entries.
# Usage: bash remove_io_cron.sh

if ! crontab -l 2>/dev/null | grep -q "nous-observatory-io26"; then
  echo "No nous-observatory-io26 cron entries found — nothing to remove."
  exit 0
fi

crontab -l 2>/dev/null | grep -v "nous-observatory-io26" | crontab -
echo "✓ Removed Google I/O 2026 cron entries."
