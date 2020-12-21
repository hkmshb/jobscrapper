#!/bin/bash


function show_help {
  echo """
    Commands
    ========
    help            : show this help
    make-html       : process docs and generate html output
  """
}

case "$1" in

  help )
    show_help
  ;;

  make-html )
    make html
  ;;

  * )
    /bin/sh -c $@
  ;;

esac
