#!/bin/bash

set -o errexit

LOGFILE="$HOME/docker_prune.log"

{
  echo "Starting Docker system prune at $(date)"
  sudo /usr/bin/docker system prune -f
  echo "Pruned Docker objects successfully"

  echo "Starting Docker volume prune at $(date)"
  sudo /usr/bin/docker system prune --volumes -f
  echo "Pruned Docker volumes successfully"
  echo "Completed at $(date)"
} >> "$LOGFILE" 2>&1
