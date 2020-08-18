#!/bin/sh

echo "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n >> waiting on postgres\n"
/app/wait-for.sh ${DJAPP_DBHOST}:${DJAPP_DBPORT} -- echo "postgres is up!"

echo "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n >> starting cron\n"
env >> /etc/environment
service cron start

# run django migrations
echo "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n >> running db migrations\n"
python webapp/manage.py migrate

# run the django application
echo "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n >> running webapp\n"
python webapp/manage.py runserver 0.0.0.0:8000
