#!/bin/bash

virtualenv --no-site-packages ve
. ve/bin/activate
pip install -r requirements.pip
deactivate
