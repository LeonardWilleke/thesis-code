#!/bin/sh
set -e -u

fmi_settings_path='../cases/flow-around-mounted-cylinder-controlled/controller-fmi/fmi-settings.json'
precice_settings_path='../cases/flow-around-mounted-cylinder-controlled/controller-fmi/precice-settings.json'

python3 ../../../runner/runner.py $fmi_settings_path $precice_settings_path
