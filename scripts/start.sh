#!/bin/sh

echo "================================"
echo "Starting the application..."
echo "================================"

echo ""
echo "[1/6] Waiting for Redis..."

until nc -z redis 6379; do
    echo "Waiting for Redis to be available..."
    sleep 1
    done

echo "redis is up"

echo ""
echo "[2/6] Applying migrations..."
python manage.py migrate --noinput

echo ""
echo "[3/6] Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "[4/6] Compiling translations..."
django-admin comilemessages || true

echo ""
echo "[5/6] checking Django configuration..."
python manage.py check --deploy

echo ""
echo "[6/6] Starting server..."


python manage.py runserver 0.0.0.0:8000