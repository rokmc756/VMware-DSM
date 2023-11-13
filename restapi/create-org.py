#!/usr/bin/python3
import requests
import json
import uuid
import urllib3
urllib3.disable_warnings()

# import pdb
# pdb.set_trace()

import logging
# import httplib
import http.client

# Debug logging
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True


# https://dsm-provider.jtest.pivotal.io/provider/swagger-ui/index.html
# DSM API endpoint URL for authentication
auth_url = "https://dsm-provider.jtest.pivotal.io/provider/session"
# auth_url = "https://dsm-provider.jtest.pivotal.io/appliance/provider/password"

# Your DSM credentials
username = "jomoon@pivotal.io"
password = "Changeme12!@"

# Authentication payload
auth_payload = {
    "email": username,
    "password": password
}

l_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

try:
    # Send a POST request to authenticate and obtain the Bearer token
    response = requests.post(auth_url, json=auth_payload, headers=l_headers, verify=False)

    if response.status_code == 200:
        # Retrieve the Bearer token from the response headers
        bearer_token = response.headers.get('Authorization')
        eh = response.headers.get('Access-Control-Expose-Headers')
        # print(f"Bearer Token: {bearer_token}")
    else:
        print(f"Authentication failed. Status code: {response.status_code}")
        # print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")

#for x in response.headers:
#  print(x)


# my_json_str = json.dumps(eh)
# d = json.loads(my_json_str)
# print(eh)
# exit()

# print(response.text)
# print(response.json())

my_json_str = json.dumps(response.json())
d = json.loads(my_json_str)

# print(my_json_str)             # 👉️ '{"name": "Bobby Hadz", "age": 30}'
# print(type(my_json_str))       # 👉️ <class 'str'>
#

# print(f"Org ID: {d['orgMemberships']['orgId']}")
# print(f"First Name: {d['firstName']}") - OK
# print(f"Org ID: {d['orgMemberships'][0]['orgId']}")


# print(f"X Org ID: {eh[0]}")

# my_org_id = f"Org ID: {d['orgMemberships'][0]['orgId']}"
my_org_id = f"{d['orgMemberships'][0]['orgId']}"

# DSM API access token
access_token = bearer_token

#  "ldapOrgDetails": [],
org_data = {
  "companyName": "VMware_Tanzu",
  "email": "romooon@pivotal.io",
  "instanceMode": "FREE_MODE",
  "dbFqdnSuffix": "jtest.vmware.com"
}


# User data to be created
user_data = {
    "firstName": "Rose",
    "lastName": "Moon",
    "contactNumber": "010-6481-1998",
    "email": "romoon@pivotal.io",
    "password": "Changeme12!@",
    "roles": [
      "PROVIDER"
    ]
}

#    "tenantId": "b78d5e8c-5dcd-409d-96ee-ee6556632e70",
#      "PROVIDER_ORG"

# print(access_token)
#    headers = {'Authorization': f'Bearer {access_token}'}
#    "Authorization": access_token,
#    headers = {'Authorization': f'Bearer {access_token}'}
#    "Authorization": bearer_token,
#    'Authorization': f"Bearer {access_token}",
#    "Authorization': "{access_token}",
#    "X-Org-ID": my_org_id
#t_headers = {
#    "Authorization": access_token,
#    "X-Org-ID": my_org_id
#}


# print(my_org_id)

# 352 page, https://docs.vmware.com/en/VMware-Data-Services-Manager/1.5/data-services-manager.pdf
#    "Accept": "application/vnd.vmware.dms-v1+json",
#    "Content-Type": "application/json",
#    "Accept": "*/*",
#    "Accept": "application/json",
#    "Content-Type": "application/json",
#    "Accept": "application/vnd.vmware.dms-v1+json",
#    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#    "Content-Type": "application/json",
#    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#    "Authorization": access_token,
#    "Accept": "application/json",
t_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"{bearer_token}",
    "X-Org-ID": my_org_id
}

org_url = "https://dsm-provider.jtest.pivotal.io/provider/orgs"
# print(t_headers)

try:
    # Send a POST request to create the user
    # response = requests.post(auth_url, json=auth_payload, headers=headers, data=json.dumps(user_data), verify=False)
    response = requests.post(org_url, headers=t_headers, data=json.dumps(org_data), verify=False)
    # response = requests.post(org_url, data=json.dumps(org_data), verify=False)

    if response.status_code == 201:
        print("User created successfully.")
    else:
        print(f"Failed to create org. Status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")

#
# https://stackoverflow.com/questions/45726404/how-to-add-access-control-expose-headers-in-nginx-server
# vi /etc/nginx/nginx-tdm.conf
# ~~ snip
# add_header 'Access-Control-Expose-Headers' 'X-Requested-With,Content-Type,Authorization,Origin,Accept,Access-Control-Request-Method,Access-Control-Request-Headers,Access-Control-Expose-Headers,Content-Disposition,X-Org-ID';
# ~~ snip
