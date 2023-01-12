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
  log "INFO" "### Installing ${SERVICE_NAME} ###"
  
  # if [[ ${LB_EXTERNEL_IP} == "" ]]; then
  #   log "INFO" "### Please input external load balancer IP ###"
  #   read -p 'IP address: ' LB_EXTERNEL_IP
  # fi

  if [[ ${ret_val} -eq 0 ]]; then
    log "INFO" "Installing ${SERVICE_NAME} with Helm"
    helm upgrade ${SERVICE_NAME} ${HELM_TEMPLATE_PATH} \
      --values ${HELM_TEMPLATE_PATH}values.yaml \
      --create-namespace \
      --namespace ${SERVICE_NAMESPACE} \
      --install \
      --wait \
      --timeout=300s #\
      # --set loadBalancer.ip=${LB_EXTERNEL_IP}
  fi
}

main "$@"
