#!/bin/sh

echo ">> waiting on postgres"
/app/wait-for.sh ${DJAPP_DBHOST}:${DJAPP_DBPORT} -- echo "postgres is up!"

# run django migrations
python webapp/manage.py migrate

# run the django application
python webapp/manage.py runserver 0.0.0.0:8000
