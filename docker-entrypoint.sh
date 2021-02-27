#!/usr/bin/env bash

echo "Applying DB migrations..."
python manage.py migrate

echo "Loading fixtures..."
python manage.py loaddata fixtures.yaml --format yaml

echo "Syncing role permissions..."
python manage.py sync_roles --reset_user_permissions

"$@"
