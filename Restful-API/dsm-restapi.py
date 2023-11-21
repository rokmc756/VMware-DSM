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
plan_url = "https://dsm-provider.jtest.pivotal.io/provider/instancetype"
storage_url = "https://dsm-provider.jtest.pivotal.io/provider/storagesettings"
s3_url = "https://dsm-provider.jtest.pivotal.io/provider/s3storages"

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
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

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
            print("Organization created successfully")
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
# def create_plan(plan_url, access_token, x_org_id, tenant_id):
def create_plan(plan_url, access_token, x_org_id):

    print("Create Plan...")

    plan_data = {
      "name": "jPlan01",
      "cpu": 2,
      "memory": 4
    }

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(plan_url, headers=token_headers, data=json.dumps(plan_data), verify=False)

        if r.status_code == 200:
            print("Plan created successfully.")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create plan. Status code: {r.status_code}")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")

#


def create_storage(storage_url, access_token, x_org_id):

    print("Create Storage...")

    storage_data = {
      "storageType": "PROVIDERREPO",
      "url": "https://minio.jtest.pivotal.io:9000",
      "accessKey": "minioadmin",
      "secretKey": "changeme",
      "bucket": "jbucket01",
      "region": "",
      "thumbprint": "05:ba:0c:8d:fd:0a:8d:c6:72:e1:11:f9:1b:db:98:53:84:38:ce:f9:0d:81:73:da:db:7a:bb:74:b5:12:f8:d9"
    }
    # Need to know how to get thumbprint

    #  "region": "",
    #  "defaultRepo": True

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(storage_url, headers=token_headers, data=json.dumps(storage_data), verify=False)

        if r.status_code == 200:
            print("Plan created successfully")
            # print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create storage. Status code: {r.status_code}")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")

#

# Provider log repo
def create_storage1(storage_url, access_token, x_org_id):

    print("Create Storage...")

    storage1_data = {
      "storageType": "PROVIDER_LOG_REPO",
      "url": "https://minio.jtest.pivotal.io:9000",
      "accessKey": "minioadmin",
      "secretKey": "changeme",
      "bucket": "jbucket02",
      "region": "",
      "thumbprint": "05:ba:0c:8d:fd:0a:8d:c6:72:e1:11:f9:1b:db:98:53:84:38:ce:f9:0d:81:73:da:db:7a:bb:74:b5:12:f8:d9"
    }
    # Need to know how to get thumbprint

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(storage_url, headers=token_headers, data=json.dumps(storage1_data), verify=False)

        if r.status_code == 200:
            print("Plan created successfully")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create storage. Status code: {r.status_code}")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")



# Provider backup repo
def create_storage2(storage_url, access_token, x_org_id):

    print("Create Storage...")

    storage2_data = {
      "storageType": "PROVIDER_BACKUP_REPO",
      "url": "https://minio.jtest.pivotal.io:9000",
      "accessKey": "minioadmin",
      "secretKey": "changeme",
      "bucket": "jbucket03",
      "region": "",
      "thumbprint": ""
    }
    #  "thumbprint": "05:ba:0c:8d:fd:0a:8d:c6:72:e1:11:f9:1b:db:98:53:84:38:ce:f9:0d:81:73:da:db:7a:bb:74:b5:12:f8:d9"
    # Need to know how to get thumbprint

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(storage_url, headers=token_headers, data=json.dumps(storage2_data), verify=False)

        if r.status_code == 200:
            print("Plan created successfully")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create storage. Status code: {r.status_code}")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")

# Provider backup repo
def create_s3_storage1(s3_url, access_token, x_org_id):

    print("Create s3 Storage...")

    # b = uuid4()
    # print(json.dumps({'a': str(b)}))
    #   "id": json.dumps({'a': str(uuid.uuid4())}),
    #  "id": x_org_id,
    #  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    s3_data1 = {
      "name": "s3test01",
      "endpoint": "https://minio.jtest.pivotal.io:9000",
      "bucket": "jbucket04",
      "accessKey": "minioadmin",
      "secretKey": "changeme",
      "region": "",
      "thumbprint": "05:ba:0c:8d:fd:0a:8d:c6:72:e1:11:f9:1b:db:98:53:84:38:ce:f9:0d:81:73:da:db:7a:bb:74:b5:12:f8:d9",
      "templateStorage": True
    }
    # Need to know how to get thumbprint

    token_headers = {
      "Accept": "application/vnd.vmware.dms-v1+json",
      "Authorization": f"Bearer {access_token}",
      "X-Org-ID": x_org_id,
      "Content-Type": "application/json"
    }

    try:
        r = requests.post(s3_url, headers=token_headers, data=json.dumps(s3_data1), verify=False)

        if r.status_code == 200:
            print("s3 storage created successfully")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
        else:
            print(f"Failed to create s3 storage. Status code: {r.status_code}")
            print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    except Exception as e:
        print(f"An error occurred: {e}")


#
def main():

    access_token, org_id = login_dsm(login_url,dsm_api_login,dsm_api_password)
    # create_org(orgs_url,access_token,org_id)
    # tenant_id = get_org(orgs_url,access_token,org_id)
    # create_user(users_url,access_token,org_id,tenant_id)
    # create_plan(plan_url,access_token,org_id)
    # create_storage(storage_url,access_token,org_id)
    # create_storage1(storage_url,access_token,org_id)
    #create_storage2(storage_url,access_token,org_id)
    # print(uuid.uuid4())
    create_s3_storage1(s3_url,access_token,org_id)

    # print(access_token)
    # print(org_id)
    # print(tenant_id)

#
if __name__ == '__main__':
    main()

# https://dsm-provider.jtest.pivotal.io/provider/swagger-ui/index.html
