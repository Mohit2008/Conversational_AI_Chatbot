#!/bin/bash

set -e

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$MYDIR/create_venv.sh
source ${MYDIR}/venv/bin/activate

export PACKAGE_VERSION="1.0.0"

rm -rf $MYDIR/chatbot*.tar || true
DISTDIR=$MYDIR/dist
rm -f $DISTDIR/*

pip3 wheel $MYDIR -w $DISTDIR

pushd $MYDIR
tar cvf chatbot_${PACKAGE_VERSION}.tar dist/chatbot*.whl
popd