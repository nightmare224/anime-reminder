#!/bin/bash

ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

### Load conf/config.ini configuration file ###
source <(grep = config.ini)

function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {

  log "INFO" "Installing ${SERVICE_NAME} with yaml file"
  # kubectl apply -f deploy.yaml
  helm upgrade ${SERVICE_NAME} ${HELM_TEMPLATE_PATH} \
    --values ${HELM_TEMPLATE_PATH}values.yaml \
    --create-namespace \
    --namespace ${SERVICE_NAMESPACE} \
    --install \
    --wait \
    --timeout=600s \
    --set loadBalancer.ip=${LB_EXTERNEL_IP}
}

main "$@"
