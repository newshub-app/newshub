#!/bin/sh

if [ "${NEWSHUB_BOOTSTRAP}" = "yes" ]
then
  python manage.py collectstatic --noinput
  /wait
  python manage.py migrate
  python manage.py loaddata categories
  python manage.py tasksinit
else
  /wait
fi

exec "$@"
