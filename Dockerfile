## The base image to build the new image from. This is an Alpine linux image
## WITH Python version 3.8 already installed.
FROM python:3.8-alpine

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
RUN apk add --no-cache \
        gcc \
        musl-dev \
        postgresql-dev

## Create a local user and group to run the application under. It is not ideal
## to use the root user with root privileges to run an application. It is best
## practice to use a User with the least amount of privileges necessary to run
## an application successfully. `addgroup` and `adduser` commands use the value
## from environment variables set above.
RUN addgroup -g 92 -S ${APP_USER} && \
    adduser -u 92 -h /app -H -D -S -G ${APP_USER} ${APP_USER}

## Copy and embed the requirements.txt file and the webapp folder into the
## image all within the `/app` folder of the image.
COPY ./requirements.txt /app/
COPY ./webapp /app/webapp

## Update pip, then install all Python dependencies for the application into
## the image using the requirements.txt file within the image.
RUN pip install --upgrade pip &&\
    pip install --no-cache -r /app/requirements.txt

## Copy the bash script to running the Djangoo application named start.sh to
## the `/app` folder inside the image.
COPY ./scripts/start.sh /app/start.sh

## Change the mode of the copied start.sh script to set the file as executable
RUN chmod +x /app/start.sh

## Set the container user as the user configured with an environment variable
## and created above. The docker instructions that follow are executed as the
## set user.
USER ${APP_USER}

## Expose the port the Django application is handling requests on so that it
## can be bounded to a host port so the application is accessible through the
## host port to docker port binding.
EXPOSE ${PORT}

## Indicates the command to run on starting up a container from the built image.
## The start.sh bash script is executed as the user set above when the container
## starts up.
CMD ["/app/start.sh"]
