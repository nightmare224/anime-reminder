#!/bin/bash
ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}


## add certificate
APISERVER=https://kubernetes.default.svc
SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount
NAMESPACE=$(cat ${SERVICEACCOUNT}/namespace)
TOKEN=$(cat ${SERVICEACCOUNT}/token)
CACERT=${SERVICEACCOUNT}/ca.crt
curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api/v1/namespaces/cert-manager/secrets/selfsigned-root-secret 2>/dev/null | jq -r '.data."tls.crt"' | base64 -d > /usr/local/share/ca-certificates/selfsigned-root.crt
curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api/v1/namespaces/anime-reminder/secrets/selfsigned-inter-secret 2>/dev/null | jq -r '.data."tls.crt"' | base64 -d > /usr/local/share/ca-certificates/selfsigned-inter.crt
curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api/v1/namespaces/anime-reminder/secrets/anime-reminder-tls-secret 2>/dev/null | jq -r '.data."tls.crt"' | base64 -d > /usr/local/share/ca-certificates/anime-reminder.crt
update-ca-certificates

cert_path=$(python3 -m certifi 2>/dev/null)
ret_val=$?
if [[ ${ret_val} -eq 0 ]]; then
    awk '{ printf "%s", $0 }' ${cert_path} > /tmp/certifi.pem
    cert_content=$(cat /usr/local/share/ca-certificates/selfsigned-root.crt | sed 's/-----.*-----//g' | tr -d '\n')
    if ! grep -q "${cert_content}" /tmp/certifi.pem; then
        cat /usr/local/share/ca-certificates/selfsigned-root.crt /usr/local/share/ca-certificates/anime-reminder.crt >> $cert_path
    fi
fi

# run app
python3 main.py