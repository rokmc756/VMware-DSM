import json

s = '''
{
  "links": [
    {
      "rel": "self",
      "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs?page=0&size=20"
    }
  ],
  "content": [
    {
      "id": "b78d5e8c-5dcd-409d-96ee-ee6556632e70",
      "companyName": "Provider_Default",
      "email": "jomoon@pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "PROVIDER_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": null,
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/b78d5e8c-5dcd-409d-96ee-ee6556632e70"
        }
      ]
    },
    {
      "id": "4ce8cc71-9419-4d42-b6e0-a20dd720322a",
      "companyName": "test",
      "email": "test@test.co.kr",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "test.test.co.kr",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/4ce8cc71-9419-4d42-b6e0-a20dd720322a"
        }
      ]
    },
    {
      "id": "69766daa-80f3-4ec8-953d-d6ec8b7255b9",
      "companyName": "VMware_Tanzu",
      "email": "jomoon@jtest.pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "jtest.vmware.com",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/69766daa-80f3-4ec8-953d-d6ec8b7255b9"
        }
      ]
    },
    {
      "id": "1df94fa0-1f26-4172-9dbd-05a2e0905eb3",
      "companyName": "Tanzu_Support1",
      "email": "kimooon1@pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "jtest.vmware1.com",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/1df94fa0-1f26-4172-9dbd-05a2e0905eb3"
        }
      ]
    },
    {
      "id": "d2eb6e03-7560-413c-8172-c1cbddd591d2",
      "companyName": "Tanzu_Support2",
      "email": "kimooon2@pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "jtest.vmware2.com",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/d2eb6e03-7560-413c-8172-c1cbddd591d2"
        }
      ]
    },
    {
      "id": "b7e80018-b506-4868-b1ca-a98b820ac1e3",
      "companyName": "Tanzu_Support3",
      "email": "kimooon3@pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "jtest.vmware3.com",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/b7e80018-b506-4868-b1ca-a98b820ac1e3"
        }
      ]
    },
    {
      "id": "7831e80f-ff5c-4c20-ba06-075824ffbd41",
      "companyName": "Tanzu_Support4",
      "email": "kimooon4@pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "jtest.vmware4.com",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/7831e80f-ff5c-4c20-ba06-075824ffbd41"
        }
      ]
    },
    {
      "id": "2c4207a5-87ac-4460-9c4d-8e7e1e960de7",
      "companyName": "Tanzu_Support5",
      "email": "kimooon5@pivotal.io",
      "instanceMode": "FREE_MODE",
      "deleted": false,
      "orgType": "TENANT_ORG",
      "ldapOrgDetails": null,
      "dbFqdnSuffix": "jtest.vmware5.com",
      "links": [
        {
          "rel": "self",
          "href": "https://dsm-provider.jtest.pivotal.io/provider/orgs/2c4207a5-87ac-4460-9c4d-8e7e1e960de7"
        }
      ]
    }
  ],
  "page": {
    "size": 20,
    "totalElements": 8,
    "totalPages": 1,
    "number": 0
  }
}
'''

# data = json.loads(s)

org_obj = json.loads(s)

for org_arr in org_obj["content"]:
    if org_arr["companyName"] == "VMware_Tanzu":
        id_value = org_arr["id"]
        break
else:
    # Some default action
    id_value = "Nothing found"
    print(id_value)

print(id_value)

# https://stackoverflow.com/questions/31483655/how-to-select-specific-json-element-in-python
# https://stackoverflow.com/questions/38115290/how-to-search-for-specific-value-in-json-array-using-python

# Need test
# result = [ x for x in data if x["companyName"] == "VMware_Tanzu" ]
# result = list(map(lambda x:x if x["companyName"]=="VMware_Tanzu" , data)
