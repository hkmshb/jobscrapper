#!/bin/bash

if [ -z ${DJAPP_DBUSER} ] || [ -z ${DJAPP_DBNAME} ] || [ -z ${DJAPP_DBPASS} ]; then
  cat <<- EOF >&2
    Error: Missing environment variables required to configure database:
           DJAPP_DBNAME, DJAPP_DBUSER, DJAPP_DBPASS

    Be sure to delete the current database volume after setting these required
    environment variables, otherwise this database configuration script will
    not be run again. For more details see the Initialization scripts section
    of: https://hub.docker.com/_/postgres
EOF
  exit 1
fi

echo -e "\n***** CREATING ${DJAPP_DBUSER} ROLE *****"
psql <<- EOSQL
  CREATE ROLE "${DJAPP_DBUSER}"
  WITH LOGIN
       PASSWORD '${DJAPP_DBPASS}'
       NOSUPERUSER
       NOCREATEDB
       NOCREATEROLE;
EOSQL

echo -e "\n***** CREATING ${DJAPP_DBNAME} DATABASE *****"
psql <<- EOSQL
  CREATE DATABASE "${DJAPP_DBNAME}"
  WITH TEMPLATE template_postgis
       OWNER "${DJAPP_DBUSER}";

  CREATE DATABASE "test_${DJAPP_DBNAME}"
  WITH TEMPLATE template_postgis
       OWNER "${DJAPP_DBUSER}";
EOSQL

echo "***** ENABLE EXTENSIONS *****"
psql -d ${DJAPP_DBNAME} <<- EOSQL
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
  ALTER VIEW geometry_columns OWNER TO "${DJAPP_DBUSER}";
  ALTER TABLE spatial_ref_sys OWNER TO "${DJAPP_DBUSER}";
EOSQL
