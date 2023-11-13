import requests
import json
import urllib3
urllib3.disable_warnings()

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

try:
    # Send a POST request to authenticate and obtain the Bearer token
    response = requests.post(auth_url, json=auth_payload, verify=False)

    if response.status_code == 200:
        # Retrieve the Bearer token from the response headers
        bearer_token = response.headers.get('Authorization')
        # print(f"Bearer Token: {bearer_token}")
    else:
        print(f"Authentication failed. Status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")


# DSM API access token
# access_token = bearer_token
# print(access_token)
print(bearer_token)

org_data = {
  "companyName": "VMware Tanzu",
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
    "tenantId": "b78d5e8c-5dcd-409d-96ee-ee6556632e70",
    "roles": [
      "PROVIDER_ORG"
    ]
}

# print(access_token)

#    "Authorization": access_token,
t_headers = {
    "Authorization": bearer_token,
    "Content-Type": "application/json"
}

org_url = "https://dsm-provider.jtest.pivotal.io/orgs"
user_url = "https://dsm-provider.jtest.pivotal.io/users"

print(t_headers)

try:
    # Send a POST request to create the user
    # response = requests.post(auth_url, json=auth_payload, headers=headers, data=json.dumps(user_data), verify=False)
    # response = requests.put(auth_url, headers=headers, data=json.dumps(user_data), verify=False)
    response = requests.post(org_url, headers=t_headers, data=json.dumps(org_data), verify=False)

    if response.status_code == 201:
        print("User created successfully.")
    else:
        print(f"Failed to create user. Status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
