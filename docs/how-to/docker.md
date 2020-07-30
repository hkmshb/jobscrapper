# How-To

All `docker-compose` commands illustrated in this document are expected to be executed from
within the project root directory on the command line interface (aka cli, shell). This is the
folder directly containing the `README.md`, `docker-compose.yml` (aka compose file) files
together with other files.

---

## Table of contents

- [Build images](#build-images)
- [Run images as containers](#run-images-as-containers)
- [Stop running containers](#stop-running-containers)
- [Target a different version of PostgreSQL and PostGIS](#target-a-different-version-of-postgresql-and-postgis)
- [Delete a docker volume](#delete-a-docker-volume)

---

## Build images

To build images for services listed in the compose file run:

```bash
# build all images
docker-compose build

# build image for a specific service
docker-compose build <service-name>
```

The **database** service uses the `postgis/postgis:12-3.0-alpine` docker image and does not specify
any `Dockerfile` to drive a build, so nothing is built instead the aforementioned image is pulled
(downloaded) from [Docker Hub](https://hub.docker.com) if it doesn't already exist on the host system.

On the other hand, the **webapp** service specifies the `image` and `build` configuration options. With
the `build` option provided, `image` is interpreted as the name of the image to build, and the `build`
option (as used in the compose file) indicates the location of the `Dockerfile` containing commands
to drive the build. The `.` in `build: .` indicates the location of the `Dockerfile` for the build as
being the same as the location of the compose file, which in this case is the project root directory.

The relevant entries within the compose file that specify the the image name and target `Dockerfile`
for the **webapp** service are shown below:

```yaml
webapp:
  build: .
  image: djpgp-webapp
  ...
```

## Run images as containers

To run images for services listed in the compose file run:

```bash
# run all services
docker-compose up

# run a specific service
docker-compose up <service-name>                    # e.g: docker-compose up database

# or multiple services
docker-compose up <service-name>, <service-name>    # e.g: docker-compose up database, webapp
```

Run `docker-compose up` on the cli to start both the **database** and **webapp** services defined
in the the compose file. Logs for each of these service will be written to the cli as they startup
and afterwards while they are running. If a container cannot be created or started for any of the
services or an error occurs while already running, logs describing the error will be written on
the cli.

## Stop running containers

To stop all running containers, a shortcut is to press the `Ctrl+C` keyboard combination.
This stops all running containers but does not delete them. Subsequent executions of
`docker-compose up` will reuse these containers. Alternatively, using a separate cli, (be
sure to have changed to the project root directory) run:

```bash
# stop all containers
docker-compose down
```

This will stop and remove all running containers. Next execution of `docker-compose up` will
create new containers.

## Target a different version of PostgreSQL and PostGIS

To determine list of available PostGIS enabled PostgreSQL docker images that can be used in
the compose file, check [here](https://hub.docker.com/r/postgis/postgis) under the `Tags`
tab/page. Identify the tag for the target image and update compose file:

```yaml
# current entry
---
  database:
    image: postgis/postgis:12-3.0-alpine
    environment:
      ...

# updated entry
---
  database:
    image: postgis/postgis:<target-tag>
    environment:
      ...
```

What does `postgis/postgis` mean in `postgis/postgis:<tag>`? The first `postgis` is the account
name on [Docker Hub](https://hub.docker.com), the next `postgis` is the image name and `<tag>`
the image tag which usually carries the version and sometimes platform/distro name.

To target just PostgreSQL without PostGIS, check this official account for postgres on Docker
Hub [here](https://hub.docker.com/_/postgres).

## Delete a docker volume

In the event that an existing docker volume is to be deleted, stop all containers using the
`docker-compose down` command to ensure the containers are delete. Then run:

```bash
# syntax
docker volume rm <volume-name>

# to delete the docker volume associated with the database service for this setup
docker volume rm djpgp-database_data
```

Line `9` in the compose file names the volume associated with the `database` service on line
`28`. Lines `8 to 7` defines the volume to be created by `docker-compose`. For more details
on working with docker volumes [see this page](https://docs.docker.com/storage/volumes/).
