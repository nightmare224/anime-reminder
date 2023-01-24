#!/bin/bash
ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

## log levels: DEBUG,INFO,WARN,ERROR,FATAL ##
function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

taglist=`sed -n 's/\[v\] *//pg' taglist | tr '\n' ',' | sed 's/,$//'`
if [ -z "$taglist" ]; then
	log "INFO" -e 'No task to do.\nPlease select the task you want to do in "taglist" file.'
else
    ansible-playbook playbook.yaml -i inventory --skip-tags always --tags $taglist -e 'ansible_python_interpreter=/usr/bin/python3'
fi