#!/usr/bin/python3
#
# Managing VMware Data Service Manager by Restful API with python
# Jack, Moon <moonja@vmware.com>
#
# ChangeLog
# 2023.11.15 - Implement login and create organization initially
#

import requests
import json
import uuid
import urllib3
import logging
import http.client

# Disable to skip SSL validation
urllib3.disable_warnings()

# Debug logging
http.client.HTTPConnection.debuglevel = 0
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True

# import pdb
# pdb.set_trace()

# Parameters
dsm_api_login = "jomoon@pivotal.io"
dsm_api_password = "Changeme12!@"
login_url = "https://dsm-provider.jtest.pivotal.io/provider/session"
orgs_url = "https://dsm-provider.jtest.pivotal.io/provider/orgs"
users_url = "https://dsm-provider.jtest.pivotal.io/provider/users"

#
def login_dsm(login_url,dsm_api_login,dsm_api_password):
    print("Getting token...")

    auth_data = {
        "email": dsm_api_login,
        "password": dsm_api_password
    }

    login_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    r = requests.post(login_url, json=auth_data, headers=login_headers, verify=False)

    if r.status_code == 200:
        auth_token = r.headers.get('Authorization')
        print("Token: " + auth_token)

        # Get org
        user_json = json.dumps(r.json())
        d = json.loads(user_json)
        org_id = f"{d['orgMemberships'][0]['orgId']}"
        print("Org ID: " + org_id)
        # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

        return auth_token, org_id

    else:
        # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

#
def create_org(orgs_url, access_token, x_org_id):
    print("Create Organization...")

    org_data = {
      "companyName": "Tanzu_Support5",
      "email": "kimooon5@pivotal.io",
      "instanceMode": "FREE_MODE",
      "dbFqdnSuffix": "jtest.vmware5.com"
    }

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(orgs_url, headers=token_headers, data=json.dumps(org_data), verify=False)

        if r.status_code == 200:
            print("Organization created successfully.")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create org. Status code: {r.status_code}")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")

#
def get_org(orgs_url, access_token, x_org_id):
    print("Get Organization ID...")

    org_data = {
      "companyName": "Tanzu_Support5",
      "email": "kimooon5@pivotal.io",
      "instanceMode": "FREE_MODE",
      "dbFqdnSuffix": "jtest.vmware5.com"
    }

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id
    }

    org_id_url = "https://dsm-provider.jtest.pivotal.io/provider/orgs" + "?page=0&size=20"

    try:
        r = requests.get(org_id_url, headers=token_headers, data=json.dumps(org_data), verify=False)

        if r.status_code == 200:
            print("Organizations got successfully.")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
            org_obj = json.loads(r.text)

            for org_arr in org_obj["content"]:
                if org_arr["companyName"] == "VMware_Tanzu":
                    id_value = org_arr["id"]
                    break
                else:
                    id_value = "Nothing found"

            # print(id_value)
            return id_value

        else:
            print(f"Failed to create org. Status code: {r.status_code}")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")

#
def create_user(orgs_url, access_token, x_org_id, tenant_id):

    print("Create User...")

    user_data = {
      "firstName": "Kid",
      "lastName": "Moon",
      "contactNumber": "010-6481-1998",
      "email": "kimoon@pivotal.io",
      "password": "Changeme12!@",
      "tenantId": tenant_id,
      "roles": [
        "ORG_ADMIN"
      ]
    }

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(users_url, headers=token_headers, data=json.dumps(user_data), verify=False)

        if r.status_code == 200:
            print("User created successfully.")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create user. Status code: {r.status_code}")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")

#
def main():

    access_token, org_id = login_dsm(login_url,dsm_api_login,dsm_api_password)
    # create_org(orgs_url,access_token,org_id)
    tenant_id = get_org(orgs_url,access_token,org_id)
    create_user(users_url,access_token,org_id,tenant_id)

    # print(access_token)
    # print(org_id)
    # print(tenant_id)

#
if __name__ == '__main__':
    main()

# https://dsm-provider.jtest.pivotal.io/provider/swagger-ui/index.html
