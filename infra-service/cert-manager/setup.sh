#!/bin/bash

ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

## log levels: DEBUG,INFO,WARN,ERROR,FATAL ##
function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

function check_namespace() {
  [ $# -eq 0 ] && log "ERROR" "No arguments supplied (check_namespace)" && exit 1
  kubectl get ns ${1} > /dev/null 2>&1
  local ret_val=$?
  echo $ret_val
}

function create_namespace() {
  [ $# -eq 0 ] && log "ERROR" "No arguments supplied (create_namespace)" && exit 1
  kubectl create namespace ${1} > /dev/null 2>&1
  local ret_val=$?
  echo $ret_val
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
   if [[ $# -ge 3 ]]; then
      SERVICE_NAMESPACE=$1
      SERVICE_NAME=$2
      DOMAIN_NAME=$3
   else 
      log "ERROR" "Input error, please check input arguments"
      exit 1
   fi

   ret_val="$(check_namespace ${SERVICE_NAMESPACE})"
   if [[ ${ret_val} != 0 ]]; then
      log "WARN" "The namespace ${SERVICE_NAMESPACE} not found"
      log "INFO" "Create namespace [${SERVICE_NAMESPACE}] in the k8s"

      ret_val="$(create_namespace ${SERVICE_NAMESPACE})"
      if [[ ${ret_val} -eq 0 ]]; then
         log "INFO" "The ${SERVICE_NAMESPACE} namespace was created successfully"
      fi
   fi

   ## create issure.yaml
cat <<EOF > ./${SERVICE_NAME}-issuer.yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
   name: ${SERVICE_NAME}-self-sign-issuer-tls
   namespace: ${SERVICE_NAMESPACE}
spec:
   selfSigned: {}
EOF
   deploy ${SERVICE_NAME}-issuer.yaml
   rm -f ${SERVICE_NAME}-issuer.yaml


   ## Create cert.yaml
cat <<EOF > ./${SERVICE_NAME}-cert.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
   name: ${SERVICE_NAME}-cert
# the ns should be the same as service's
   namespace: ${SERVICE_NAMESPACE}
spec:
# name of the tls secret to store the generated certificate/key pair
   secretName: ${SERVICE_NAME}-tls-secret
   isCA: true
   issuerRef:
      name: ${SERVICE_NAME}-self-sign-issuer-tls
      kind: Issuer
   commonName: "${SERVICE_NAME}-signed-ca"
   duration: 175200h0m0s
   renewBefore: 24h0m0s
   dnsNames:
   - ${DOMAIN_NAME}
EOF
   deploy ${SERVICE_NAME}-cert.yaml
   rm -f ${SERVICE_NAME}-cert.yaml

   log "INFO" "Deploy ${SERVICE_NAME} issuer & certificate success."
}

main "$@"