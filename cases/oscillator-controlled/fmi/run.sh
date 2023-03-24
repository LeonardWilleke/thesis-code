#!/bin/sh
set -e -u

fmi_settings_path='../cases/oscillator-controlled/fmi/fmi-settings.json'
precice_settings_path='../cases/oscillator-controlled/fmi/precice-settings.json'

python3 ../../../runner/runner.py $fmi_settings_path $precice_settings_path
