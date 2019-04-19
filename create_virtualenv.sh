#!/usr/bin/env bash
set -eo pipefail

pip3 install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt