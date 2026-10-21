#!/bin/bash

set -o errexit
set -o nounset

LOGFILE="$HOME/docker_prune_cron.log"

current_date=$(date -Iseconds)

{
  echo "Starting Docker system prune at $current_date"
  sudo docker system prune --volumes --force
  echo "Completed at $(date -Iseconds)"
} >> "$LOGFILE" 2>&1
