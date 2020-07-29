FROM python:3.8-alpine

LABEL maintainer="Abdul-Hakeem <hkmshb@gmail.com>"

ENV APP_USER=webapp
ENV PORT=8000

## set up working directory
RUN mkdir /app
WORKDIR /app

## install system dependencies
RUN apk add --no-cache \
        gcc \
        musl-dev \
        postgresql-dev

## create a local user and group to run the app
RUN addgroup -g 92 -S ${APP_USER} && \
    adduser -u 92 -h /app -H -D -S -G ${APP_USER} ${APP_USER}

## install dependencies
COPY ./requirements.txt /app/
COPY ./webapp /app/webapp

RUN pip install --upgrade pip &&\
    pip install --no-cache -r /app/requirements.txt

## set up entrypoint
COPY ./scripts/start.sh /app/start.sh
RUN chmod +x /app/start.sh

RUN echo $(pwd)
RUN echo $(ls -al `pwd`)

# USER webapp
EXPOSE ${PORT}

CMD ["/app/start.sh"]
