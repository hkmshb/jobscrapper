#!/bin/bash


function show_help {
  echo """
    Commands
    ========
    help            : show this help
    loadsample      : load sample companies and openings data
    manage ...      : django management script
    manage tests    : run available unit tests for the setup
  """
}

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

  help )
    show_help
  ;;

  loadsample )
    case "$2" in
      --companies )
        python webapp/manage.py loaddata companies.json locations.json
      ;;

      --openings )
        python webapp/manage.py loaddata openings.json
      ;;

      * )
        python webapp/manage.py loaddata companies.json locations.json
        python webapp/manage.py loaddata openings.json
      ;;
    esac
  ;;

  manage )
    run_manage "${@:2}"
  ;;

  * )
    /bin/sh -c $@
  ;;

esac
