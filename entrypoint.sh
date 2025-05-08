#!/bin/bash

set -e  # exit on error
echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

SCRIPT_FLAG="/app/.script_ran_once"

if [ ! -f "$SCRIPT_FLAG" ]; then
  echo "Running custom script..."
  python manage.py fetch_save_data_to_database
  touch "$SCRIPT_FLAG"
fi

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 countries_api.wsgi:application