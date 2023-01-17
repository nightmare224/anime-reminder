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
function deploy() {
  rsp=$(kubectl create -f ${1} 2>&1)
  rsp_val=$?
  if [[ ${rsp_val} != 0 ]]; then
    ## If service exsit, bypass error
    if [[ ${rsp} == *"AlreadyExists"* ]]; then
      log "WARN" "${rsp}"
    else
      log "ERROR" "Deploy ${1} error"
      log "ERROR" "${rsp}"
      exit 1
    fi
  else
    log "INFO" "Deploy an ${1} success."
  fi
}

main() {

  log "INFO" "Installing ${SERVICE_NAME} with Helm"
  # would stuck with no reason, but still work normally
  helm upgrade ${SERVICE_NAME} ${HELM_TEMPLATE_PATH} \
    --values ${HELM_TEMPLATE_PATH}values.yaml \
    --create-namespace \
    --namespace ${SERVICE_NAMESPACE} \
    --install \
    --wait \
    --timeout=60s 2>/dev/null
  
  log "INFO" "Deploy an self-sign Issuer."
  deploy ${ISSUER_PATH}/self-sign-issuer.yaml

  log "INFO" "Deploy Certificate Object requesting certificate from self-sign issuer"
  deploy ${ISSUER_PATH}/certificate.yaml
  
  log "INFO" "Deploy an Issuer equipped with the certificate signed by self-sign issuer"
  deploy ${ISSUER_PATH}/ca-issuer.yaml
}

main "$@"
