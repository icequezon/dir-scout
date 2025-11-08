#!/bin/bash

echo "Starting Dir-Scout..."
echo "Redis URL: $REDIS_URL"
echo "Redis Port: $REDIS_PORT"
echo "Redis Stream: $REDIS_STREAM"

EVENTS="-e create -e modify -e delete -e close_write -e moved_to"

EXCLUDE_REGEX='--exclude "/\.[^/]+$"'
if [ "$INCLUDE_DOTFILES" = "true" ] || [ "$INCLUDE_DOTFILES" = "TRUE" ]; then
    echo "[inotify] INCLUDE_DOTFILES enabled — watching dotfiles too"
    EXCLUDE_REGEX=""
else
    echo "[inotify] Excluding dotfiles (default)"
fi


WATCH_DIR="/watched"

if [ -n "$EXCLUDE_REGEX" ]; then
    CMD="inotifywait -m -r $WATCH_DIR $EXCLUDE_REGEX $EVENTS"
else
    CMD="inotifywait -m -r $WATCH_DIR $EVENTS"
fi

echo "Watching directory recursively: $WATCH_DIR"
source .venv/bin/activate

eval "$CMD" |
while read path action file; do
  echo "Detected $action on $file in $path"
    python main.py "$path$file" "$action"
done
