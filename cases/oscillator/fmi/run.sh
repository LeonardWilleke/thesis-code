#!/bin/sh
set -e -u

usage() { echo "Usage: cmd [-l] [-r]" 1>&2; exit 1; }

# Check if no input argument was provided
if [ -z "$*" ] ; then
	usage
fi

fmi_settings_path_left='../cases/oscillator/fmi/MassLeft/fmi-settings.json'
precice_settings_path_left='../cases/oscillator/fmi/MassLeft/precice-settings.json'

fmi_settings_path_right='../cases/oscillator/fmi/MassRight/fmi-settings.json'
precice_settings_path_right='../cases/oscillator/fmi/MassRight/precice-settings.json'

# Select appropriate case
while getopts ":lr" opt; do
  case ${opt} in
  l)
    
    #python3 ../../../runner/runner.py $fmi_settings_path_left $precice_settings_path_left
    fmiprecice ./MassLeft/fmi-settings.json ./MassLeft/precice-settings.json
    python3 calculate-error.py ./MassLeft/fmi-settings.json ./MassLeft/precice-settings.json ./MassRight/fmi-settings.json ./MassRight/precice-settings.json Mass-Left

    ;;
  r)
  	
    #python3 ../../../runner/runner.py $fmi_settings_path_right $precice_settings_path_right
    fmiprecice ./MassRight/fmi-settings.json ./MassRight/precice-settings.json
    python3 calculate-error.py ./MassLeft/fmi-settings.json ./MassLeft/precice-settings.json ./MassRight/fmi-settings.json ./MassRight/precice-settings.json Mass-Right

    ;;
  *)
    usage
    ;;
  esac
done
