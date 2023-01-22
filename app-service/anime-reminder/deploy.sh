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

  LB_EXTERNEL_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

  log "INFO" "Installing ${SERVICE_NAME} with Helm"
  helm upgrade ${SERVICE_NAME} ${HELM_TEMPLATE_PATH} \
    --values ${HELM_TEMPLATE_PATH}values.yaml \
    --create-namespace \
    --namespace ${SERVICE_NAMESPACE} \
    --install \
    --wait \
    --timeout=600s \
    --set postgresql.postgresql.username=${POSTGRESQL_USER} \
    --set postgresql.postgresql.password=${POSTGRESQL_PASSWORD} \
    --set keycloak.admin.username=${KEYCLOAK_USER} \
    --set keycloak.admin.password=${KEYCLOAK_PASSWORD} \
    --set loadBalancer.ip=${LB_EXTERNEL_IP}
}

main "$@"
