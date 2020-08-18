#!/bin/bash

function run_manage {
  if [[ "$1" == "tests" ]]; then
    # install dev dependencies before running tests
    pipenv install --dev --deploy --system
    python webapp/manage.py test --keepdb ./webapp/**/tests
  else
    python webapp/manage.py $@
  fi
}

case "$1" in

  manage )
    run_manage "${@:2}"
  ;;

  * )
    /bin/sh -c $@
  ;;

esac
