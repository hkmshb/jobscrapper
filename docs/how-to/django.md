# Django Setup

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
    - [Installation using pip + virtualenv](#installation-using-pip-virtualenv)
    - [Installation using Pipenv](#installation-using-pipenv)
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

To begin, rename the `.env` file to `.env.sh` and add the `export` command before every defined
variable in the file, eg:

```ini
  # previous content
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

The PostgreSQL + PostGIS database configure with the compose file can be started and connected to
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

#### Installation using pip + virtualenv

Proceed as follows (remember to run commands from the project root directory):

```bash
# create a virtualenv name `.venv` using Python venv module available in Python 3.6+
python3 -m venv .venv

# activate virtualenv
. ./.venv/bin/activate

# install python dependencies for the project
(.venv) pip install -r requirements.txt

# export all environment variables into the shell
(.venv) source .env.sh

# run the application
(.venv) python webapp/manage.py runserver 8080
```

Access the running Django application at <http://localhost:8080/> on your browser.

#### Installation using Pipenv

Unlike `pip` which comes with Python, [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)
needs to be installed. With `Pipenv` you no longer need to use `pip` and `virtualenv` separately.
They work together. On MacOS and Linux (using Linuxbrew), use the command below to install `Pipenv`
as a command-line tool available system wide.

```bash
brew install pipenv
```

Alternatively, pipenv can be installed using `pip`. See `Pipenv` [installation guide](
https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv) for more details.

```bash
pip install pipenv
```

Proceed as follows (remember to run commands from the project root directory):

```bash
# install all python dependencies for the project from the Pipfile (and Pipfile.lock)
# A virtualenv is created (and used) automatically
pipenv install

# verify location of created virtualenv (optional)
pipenv --venv

# run the application
# NOTE: there is no need to create a separate `.env.sh` file with `export` command
# added before each variable. Pipenv has in-built support for automatically loading
# and working with `.env` files if any exists.
pipenv run webapp/manage.py runserver 8081
```

Access the running Django application at <http://localhost:8081/> on your browser.

## Add more Django apps

Issue the command below to add a new Django app.

```bash
# it is assumed that the current directory is the project root directory
# so change into the `webapp` folder to create new app therein
cd webapp

# use manage.py
python manage.py startapp <name>

# or django-admin
django-admin startapp <name>

# return to the project root directory afterwards as most commands are expected
# to be issued from that location
cd ..
```

A Django app by the specified name is created at the current directory. Don't forget
to register the url routes for this app within the `webapps/urls.py` module.

## Install more Python third-party libraries

Add a third-party library using `pip` as follows:

```bash
# install library
pip install <library-name>

# update requirements.txt file
pip freeze > requirements.txt
```

Using `pipevn`:

```bash
# install library
pipenv install <library-name>
```

The library is automatically recorded within the `Pipfile` as a dependency for this project and
the dependencies for the installed library are captured within `Pipfile.lock`.

Rebuild the **webapp** image using `docker-compose build --no-cache webapp`. Remember to update
the `dockerfile:` entry as necessary in the compose file to reflect the target Docker file to use.
