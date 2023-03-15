#!/bin/sh
set -e -u

python3 runner.py ./pid/fmi-settings.json pid/precice-settings.json
