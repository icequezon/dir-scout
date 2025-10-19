#!/bin/bash

echo "Starting Dir-Scout..."
echo "Redis URL: $REDIS_URL"
echo "Redis Port: $REDIS_PORT"
echo "Redis Stream: $REDIS_STREAM"

WATCH_DIR="/watched"
echo "Watching directory recursively: $WATCH_DIR"
source .venv/bin/activate

inotifywait -m -r "$WATCH_DIR" |
while read path action file; do
    echo "Detected $action on $file in $path"
    python main.py "$path$file" "$action"
done
