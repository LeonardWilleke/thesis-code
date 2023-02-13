#!/bin/sh
set -e -u

usage() { echo "Usage: cmd [-l] [-r]" 1>&2; exit 1; }

# Check if no input argument was provided
if [ -z "$*" ] ; then
	usage
fi

# Select appropriate case
while getopts ":lr" opt; do
  case ${opt} in
  l)
    python3 runner.py ./MassLeft
    ;;
  r)
    python3 runner.py ./MassRight
    ;;
  *)
    usage
    ;;
  esac
done
