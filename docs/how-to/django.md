# How-To :: Django

All commands illustrated in this document are expected to be executed from within the project
root directory on the command line interface (aka cli, shell). This is the folder directly
containing the `README.md` and `docker-compose.yml` (aka compose file) files together with
other files.

---

## Table of contents

- [Run Application](#run-application)
  - [Using Docker](#using-docker)
  - [Without using Docker](#without-using-docker)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Add more Django apps](#add-more-django-apps)
- [Install more Python third-party libraries](#install-more-python-third-party-libraries)

---

## Run Application

### Using Docker

The repository is set up to run both the database and Django application using Docker. To ease
local development, the setup enables modifications to the Django project to be picked up in the
`webapp` container. Changes involving addition of new files will however require the image to be
rebuilt.

Proceed as thus to run the setup:

```bash
docker-compose up
```

### Without using Docker

The Django application provided in the `webapp` folder can be run directly on the host system
outside Docker if you so choose. Possible options are listed below and in all cases database
related environment variables need to be updated in the `.env` file as show under each section
for different options below.

To begin, rename the `.env` file to `.env.sh` and add the `export ` command before every defined
variable in the file, eg:

```ini
  # previos content
  DJAPP_DBUSER=<name>
  ...

  # updated content
  export DJAPP_DBUSER=<name>
  ...
```

#### Using PostgreSQL (with PostGIS extension) database on the host

The PostgreSQL (with PostGIS extension enabled) needs to have been installed on the host system.
The target application database can be created using [psql](https://www.postgresql.org/docs/12/app-psql.html)
or [pgAdmin](https://www.pgadmin.org) all running locally on the host system. No need to run the
`create_db.sh` bash script.

```ini
# .env.sh updates
...
export DJAPP_DBHOST=localhost
export DJAPP_DBPORT=5432
...
export ALLOWED_HOSTS='localhost'
export DEBUG=True
export SECRET_KEY=<secret>
```

#### Using SQLite database

An SQLite database would have been a viable alternative if the project does not aim to store and
manage spatial data. For this project this is not an option.

#### Using Docker database

The PostgreSQL + PostGIS databse configure with the compose file can be started and connected to
from the Django application running from the host system.

```ini
# .env.sh updates
...
export DJAPP_DBHOST=localhost
export DJAPP_DBPORT=9876
...
export ALLOWED_HOSTS='localhost'
export DEBUG=True
export SECRET_KEY=<secret>
```

#### Prerequisites

- Python 3.6+

#### Installation

Proceed as follows (remember to run commands from the project run directory):

```bash
# create a virtualenv name `.venv` using Python venv module available in Python 3.6+
python3 -m venv .venv

# activate virtualenv
. ./.venv/bin/activate

# install python dependencies for the project
(.venv) pip install -r requirements.txt

# export all environment variabels into the shell
(.venv) source .env.sh

# run the application
(.venv) python webapp/manage.py runserver 8080
```

Access the running Django application at http://localhost:8080/ on your browser.

## Add more Django apps

TODO

## Install more Python third-party libraries

TODO
