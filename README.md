# Django PGPostGIS Scaffold

This repository contains a scaffold for settuing up Django with a PostgreSQL + PostGIS database
for data storage.

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

The `.env.template` files lists all variables required for a proper setup. These settings are used
to automatically set up a new database when starting up the database docker container.

Most of the variables are set with sample values within angle brackets. Create a copy of the template
file as shown below and update all sample values in the new `.env` file. **The new values should not
have the angle brackets**.

```bash
# create copy of .env.template named .env
# NOTE: .env files should never be commit to a repo.
cp .env.template .env
```

Configure the PostgreSQL superuser login credentials under the **PG SUPERUSER** section, and the name
of the new application database and an associated user under the **APP DATABASE** section within the
`.env` file. It is considered best practice to have a separate database user with non-admin privileges
for interacting with the application database.

## Usage

```bash
docker-compose up
```

This will:

- start a docker container for the **database** docker service
- bind the host port `9876` to the postgres port `5432` so that an application like [pgAdmin](https://www.pgadmin.org)
  installed on the host can be used to view and interact with the database inside the docker container.
- create and associate a [volume](https://docs.docker.com/storage/volumes/) named `djpgp-database_data`
  with the container if one doesn't already exist for the storage of database data files.
- create default postgres databases, configure the superuser, and create the application database and
  user using configured settings in the `.env` file.

  > **NOTE**: these settings only take effect when the container has no associated volume or when the
  > volume doesn't already have database data files. If a volume with database data files already exist,
  > these are used on all subsequent starting of the database container unless the volume is deleted.
