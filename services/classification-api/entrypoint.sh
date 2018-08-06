#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z tiles-db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

#python manage.py run -h 0.0.0.0
gunicorn -b 0.0.0.0:5000 manage:app