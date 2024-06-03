#!/bin/bash

# Wait for the database container to become healthy
until docker inspect -f '{{.State.Health.Status}}' social_media_app-master-db-1 | grep -q "healthy"; do
    >&2 echo "Database is unavailable - sleeping"
    sleep 1
done

>&2 echo "Database is healthy - running migrations"
# Run migrations
docker exec -it social_media_app-master-web-1 python manage.py makemigrations
docker exec -it social_media_app-master-web-1 python manage.py migrate

>&2 echo "Starting Django development server"
# Start the Django development server
docker exec -d social_media_app-master-web-1 python manage.py runserver 0.0.0.0:8000