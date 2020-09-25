#!/bin/bash
if [[ -n $1 ]]; then
  CMD="$@"
else
  CMD=bash
fi
docker-compose exec dashboard_db $CMD
