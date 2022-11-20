#!/bin/bash
set -e

./manage.py collectstatic --no-input

./manage.py makemigrations
./manage.py migrate
exec "$@"
