#!/bin/sh

set -e

echo "================================"
echo "GoToDo Docker Entrypoint"
echo "================================"

#wait for redis\
if [ in "$REDIS_URL" ]; then
    echo "Waiting for Redis at $REDIS_URL..."
    while ! nc -z $(echo $REDIS_URL | cut -d: -f1) $(echo $REDIS_URL | cut -d: -f2); do
        sleep 1
    done
    echo "Redis is up!"
fi

mkdir -p logs

mkdir -p locale

echo "entry init completed"

exec "$@"