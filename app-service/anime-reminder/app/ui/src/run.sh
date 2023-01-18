#!/bin/bash
ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

python3 main.py