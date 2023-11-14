# JSON DATA PUSH API by Jack Moon
# Tested with VMware Data Service Manager2013-11-14

import requests

### Parameters ###
# environmentId = '82809'
api_login = 'jomoon@pivotal.io'
api_password = 'changeme'
# base_url = "https://env-" + environmentId + ".customer.cloud.microstrategy.com/MicroStrategyLibrary/api/";
login_url = "https://dsm-provider.jtest.pivotal.io/provider/session"
orgs_url = "https://dsm-provider.jtest.pivotal.io/provider/session"


#### FUNCTIONS ###
def login(login_url,api_login,api_password):
    print("Getting token...")
    data_get = { 'username': api_login, 'password': api_password, 'loginMode': 1}

    r = requests.post(base_url + 'auth/login', data=data_get)
    if r.ok:
        authToken = r.headers['X-MSTR-AuthToken']
        cookies = dict(r.cookies)
        print("Token: " + authToken)
        return authToken, cookies
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

def get_sessions(base_url, auth_token, cookies):
    print("Checking session...")
    header_gs = {'X-MSTR-AuthToken': auth_token,
                 'Accept': 'application/json'}
    r = requests.get(base_url + "sessions", headers=header_gs, cookies=cookies)
    if r.ok:
        print("Authenticated...")
        print(r)
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

def main():
    authToken, cookies = login(base_url,api_login,api_password)
    choice = None
    while choice != "0":
        print \
        ("""
        ---MENU---
        
        0 - Exit
        1 - Generate and Print Token
        2 - Get session
        """)

        choice = input("Your choice: ") # What To Do ???
        print()
    
        if choice == "0":
            print("Good bye!")  
        elif choice == "1":
            authToken, cookies = login(base_url,api_login,api_password)
        elif choice == "2":
            get_sessions(base_url, authToken, cookies)
        else:
            print(" ### Wrong option ### ")

### Main program    
