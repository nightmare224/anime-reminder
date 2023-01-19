#!/bin/bash
ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

# add certificate
echo | openssl s_client -connect sc23.group40.io:443 -servername sc23.group40.io -showcerts 2>/dev/null | sed -n -e '/BEGIN\ CERTIFICATE/,/END\ CERTIFICATE/ p' > /usr/local/share/ca-certificates/keycloak-signed-ca.crt
update-ca-certificates
cert_path=$(python3 -m certifi 2>/dev/null)
ret_val=$?
if [[ ${ret_val} -eq 0 ]]; then
    awk '{ printf "%s", $0 }' ${cert_path} > /tmp/certifi.pem
    cert_content=$(cat /usr/local/share/ca-certificates/keycloak-signed-ca.crt | sed 's/-----.*-----//g' | tr -d '\n' )
    if ! grep -q "${cert_content}" /tmp/certifi.pem; then
        cat /usr/local/share/ca-certificates/keycloak-signed-ca.crt >> $cert_path
    fi
fi

python3 main.py