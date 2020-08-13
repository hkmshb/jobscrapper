# Django App

This repository contains a setup for Django with a PostgreSQL + PostGIS database
for data storage.

---

## Table of contents

- [Setup](#setup)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
    - [Database Settings](#database-settings)
    - [Django App Settings](#django-app-settings)
- [Usage](#usage)
- [How-To Guides](#how-to-guides)
- [Setup Overview](#setup-overview)
  - [Directory Contents](#directory-contents)
- [Fetch and Run Updates](#fetch-and-run-updates)

---

## Setup

### Dependencies

- [git](https://git-scm.com/)
- [docker](https://docs.docker.com/engine/)
- [docker-compose](https://docs.docker.com/compose/)

> Setup was tested using [Docker Desktop for Mac v2.3.0.3](https://www.docker.com/products/docker-desktop)
> which comes bundled with Engine v19.03.8 and Compose v1.25.5

### Installation

```bash
git clone https://github.com/hazeltek/django-pgpostgis.git
cd django-pgpostgis
```

### Environment Variables

The `.env.template` file lists all variables required for a proper setup. These settings are used
to automatically set up a new database when starting up the database docker container.

Most of the variables are set with sample values within angle brackets. Create a copy of the template
file as shown below and update all sample values in the new `.env` file. **The new values should not
have the angle brackets**.

```bash
# create copy of .env.template named .env
# NOTE: .env files should never be committed to a repo
cp .env.template .env
```

#### Database Settings

Configure the PostgreSQL superuser login credentials under the **PG SUPERUSER** section, and the name
of the new application database and an associated user login credentials under the **APP DATABASE**
section within the `.env` file. It is considered best practice to have a separate database user with
non-admin privileges for interacting with the application database.

More variables have been added to the **APP DATABASE** section, these variables are used by the Django
application to build a connection string used to connect to the application database.

#### Django App Settings

Configure Django specific settings that control aspects of the application as explained in the official
Django documentation found [here](https://docs.djangoproject.com/en/3.0/ref/settings/). Provided below
is a brief description of core settings configurable using the `.env` file:

```text
ALLOWED_HOSTS
    List of host/domain names (or IP addresses) that the application should handle HTTP requests for.
    When DEBUG is set to True its effective value is ['localhost', '127.0.0.1'], meaning only requests
    from the host system will be processed. Ideal for local development.

DEBUG
    Turns on/off debug mode. When set to True detailed error traceback is displayed when an exception
    occurs. This is ideal for local development. THIS SHOULD BE TURNED OFF WHEN RUN IN PRODUCTION.

SECRET_KEY
    A key used for cryptograhic signing of cookies and other Django resources. This should be set to
    a unique, unpredictable valule. DJANGO WILL REFUSE TO START IF NOT SET.

```

## Usage

```bash
docker-compose up
```

This will:

- build an image for the **webapp** docker service named `djpgp-webapp` based on the configurations and
  commands provided in the `Dockerfile` found in the project root directory.
- start a docker container for the **database** and **webapp** docker services
- bind the host port `9876` to the postgres port `5432` so that an application like [pgAdmin](https://www.pgadmin.org)
  installed on the host can be used to view and interact with the database inside the docker container.
- bind the host port `8888` to the Django development server port `8000` so that the running Django
  application can be accessed from outside the webapp docker container.
- create and associate a [volume](https://docs.docker.com/storage/volumes/) named `djpgp-database_data`
  with the database container if one doesn't already exist for the storage of database data files.
- create default postgres databases, configure the superuser, and create the application database and
  application user using configured settings in the `.env` file inside the database docker container.

  > **NOTE**: these settings only take effect when the container has no associated volume or when the
  > volume doesn't already have database data files. If a volume with database data files already exist,
  > these are used on all subsequent starting of the database container unless the volume is deleted.
  > See the [docker notes for postgres](https://hub.docker.com/_/postgres), under the Initialization
  > scripts section for more details about this.

- creates a mapped volume for the **webapp** container; the `webapp` folder on the host system within
  the project root directory is mapped (linked) to `/app/webapp` folder within the container. This
  allows local changes made to files within the `webapp` folder on the host to reflect automatically
  inside the container. This is ideal for local development and eliminates the need to constantly
  rebuild the **webapp** image in order for changed files to be included in the image and available
  within containers created from the image on subsequent runs of `docker-compose up`.

Access the Django application running within the `webapp` container at <http://localhost:8888/> from
your browser.

## How-To Guides

How-to instructions can be found within the `docs/how-to` folder.

- [Docker related instructions](docs/how-to/docker.md)
- [Django related instructions](docs/how-to/django.md)

## Setup Overview

### Directory Contents

```text
django-pgpostgis/                 : project root directory
├── docs/                         : contains .md files with how-to instructions
├── scripts/                      : contains bash scripts
|   ├── postgres/
|   |   └── create_db.sh          : bash script mounted to database service image and run during container startup
|   └── start.sh                  : bash script added to webapp service iamge and run during container startup
├── webapp/                       : django application created via `django-admin startproject webapp`
|   ├── polls/                    : django app added via `django-admin startapp poll`
|   ├── webapp/                   : contains python modules for django core settings and others for url, wsgi etc
|   └── manage.py                 : django management script
├── .editorconfig                 : contains coding style settings that can be shared across Editors and IDEs
├── .env.template                 : template file for .env file defining all env vars to run setup successfully
├── .gitignore
├── docker-compose.yml
├── Dockerfile                    : version of Dockerfile for building webapp image which uses pip
├── Dockerfile.pipenv             : version of Dockerfile for building webapp image which uses pipenv
├── Pipfile                       : list of library dependencies for the django application maintained by pipenv
├── Pipfile.lock                  : lock file generated by pipenv to accompany Pipfile
├── README.md
└── requirements.txt              : list of python dependencies for the django application
```

## Fetch and Run Updates

From within the project root directory execute the set of commands provided below to fetch, build and run the
application setup using the latest changes with the code repository within GitHub.

Remember to update the `.env` file with any newly added environment variables. Kindly refer to the latest section
within the [Changelog](./CHANGELOG.md) file to determine what the new variables are. Add the new variables and set
desired values.

```bash
# pull latest changes
git pull

# stop running containers
docker-compose down

# build new image with latest changes
docker-compose build --no-cache

# run application
docker-compose up
```

With the application running visit:

- The home page at: <http://localhost:8888/>
- The admin section at <http://localhost:8888/admin>
