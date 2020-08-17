## The base image to build the new image from. This is an Debian linux image
## with Python version 3.8 already installed.
FROM python:3.8-slim

LABEL maintainer="Abdul-Hakeem <hkmshb@gmail.com>"

## Define environment variables to be used later on within the file. These are
## also exported and available within running containers.
ENV APP_USER=webapp
ENV PORT=8000

## set up working directory within the container
RUN mkdir /app
WORKDIR /app

## Install system dependencies
## the psycopg2-binary python library which provides the driver for connecting
## and interacting with a PostgreSQL database from Python doesn't publish a
## binary version for Alpine Linux on Pypi, hence it will be build from plain
## source code files. The dependencies to aid this build are what are installed
## below. `apk` for Alpine is similar to `apt` for Ubuntu and `brew` for MacOs.
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        build-essential \
        python3-dev \
        libpq-dev \
        gdal-bin \
        procps \
        cron \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

## Create a local user and group to run the application under. It is not ideal
## to use the root user with root privileges to run an application. It is best
## practice to use a User with the least amount of privileges necessary to run
## an application successfully. `addgroup` and `adduser` commands use the value
## from environment variables set above.
RUN groupadd --gid 92 --system ${APP_USER} && \
    useradd --uid 92 --home-dir /app --gid ${APP_USER} ${APP_USER}

## Copy and embed Pipenv generated Pipfile and Pipfile.lock which contain list of
## dependencies for the project and the webapp folder into the image all inside
## the `/app` folder of the image.
COPY Pipfile Pipfile.lock /app/
COPY ./webapp /app/webapp

## create a blank .env file inside /app as this is required by django-dotenv
RUN echo "# blank .env file" > /app/.env

## Assign ownership of all contents of the `/app` folder to the application user
## without this, `pipenv install` will fail as it won't have the necessary permissions
## to create required artifacts within the `/app` folder
RUN chown -R ${APP_USER}:${APP_USER} /app

## Update pip, then install all Python dependencies for the application into
## the image using the requirements.txt file within the image.
RUN pip install --upgrade pip &&\
    pip install pipenv &&\
    # --system --deploy tells pipenv to install packages directly in the container's
    # system python rather than creating a virtualenv and installing packages into
    # the virtualenv
    pipenv install --system --deploy

## Copy the bash script named start.sh to run the Django application to the
## `/app` folder inside the image.
COPY ./scripts/start.sh /app/start.sh
COPY ./scripts/cronjobs /app/cronjobs

## Download bash script to test and wait on the availability of a TCP host and port
ADD https://github.com/eficode/wait-for/raw/master/wait-for /app/wait-for.sh

## Change the mode of the script inside `/app/` to set the files as executable
RUN chmod +x /app/*.sh &&\
    chown ${APP_USER}:${APP_USER} /app/wait-for.sh

## update crontab
RUN mkdir -p /app/log &&\
    cat /app/cronjobs >> /etc/crontab &&\
    # redirect cron logs to docker output
    ln -sf /proc/1/fd/1 /app/log/cron.log

## Set the container user as the user configured with an environment variable
## and created above. The docker instructions that follow are executed as the
## set user.

# temporarily disabled to get cron to run as root
# USER ${APP_USER}

## Expose the port the Django application is handling requests on so that it
## can be bounded to a host port so the application is accessible through the
## host port to docker port binding.
EXPOSE ${PORT}

## Indicates the command to run on starting up a container from the built image.
## The start.sh bash script is executed as the user set above when the container
## starts up.
CMD ["/app/start.sh"]
