#!/bin/bash
set -e

echo "Checking if database exists..."
if [ ! -f /app/example.db ]; then
    echo "Database not found. Initializing..."
    sqlite3 /app/example.db < /app/init_db.sql
else
    echo "Database already exists. Skipping initialization."
fi

echo "Starting Gunicorn with DEBUG log level..."
exec gunicorn --timeout 300 --log-level debug --access-logfile - --error-logfile - --bind 0.0.0.0:5000 run:app
