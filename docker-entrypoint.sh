#!/bin/sh

python manage.py collectstatic --noinput

/wait
python manage.py migrate
python manage.py loaddata categories

exec "$@"
