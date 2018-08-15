#!/bin/bash

set -e

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pip3 install virtualenv
virtualenv --system-site-packages -p python3 $MYDIR/venv
source $MYDIR/venv/bin/activate
pip3 install -e $MYDIR

