curl -k -X POST -u jomoon@pivotal.io:changeme https://dsm-provider.jtest.pivotal.io/provider/session
# curl -k --insecure -X 'GET' 'https://dsm-provider.jtest.pivotal.io/provider/session' \
# -H 'accept: application/vnd.vmware.dms-v1+json' \
# -H 'Authorization: ' \
# -H 'X-Org-ID: ' \

# curl -k --insecure -i https://dsm-provider.jtest.pivotal.io/provider/session
# curl -k --insecure -i https://dsm-provider.jtest.pivotal.io/provider/orgs

curl -k -X 'GET' 'https://dsm-provider.jtest.pivotal.io/provider/session' -H 'accept: application/vnd.vmware.dms-v1+json'  -H 'Authorization: '  -H 'X-Org-ID: ' \
-u "jomoon@pivotal.io:Changeme12!@"
