# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------

import os
import json
import requests
import base64
import time
from dotenv import load_dotenv

scope = 'trapi'

RDP_HOST = 'https://api.refinitiv.com'

access_token = None
refresh_token = None
expires_in = 0

def login_v1(username, password, app_key):
    global RDP_HOST

    if not username or not password or not app_key:
        raise TypeError('Missing required parameters')
    
    auth_url = f'{RDP_HOST}/auth/oauth2/v1/token'

    # For the Password Grant scenario
    payload=f'username={username}&password={password}&grant_type=password&scope={scope}&takeExclusiveSignOnControl=true&client_id={app_key}'

    try:
       response = requests.post(auth_url, 
                                 data=payload, 
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 verify=True,
                                 allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f'RDP Authentication exception: {e}')
        return None, None, None
    
    if response.status_code == 200:  # HTTP Status 'OK'
        print('Authentication success')
        return response.json()['access_token'], response.json()['refresh_token'], int(response.json()['expires_in'])
    if response.status_code != 200:
        print(f'RDP authentication failure: {response.status_code} {response.reason}')
        print(f'Text: {response.text}')
        raise requests.exceptions.HTTPError(f'RDP authentication failure: {response.status_code} - {response.text} ', response = response )
    
def logout(app_key, access_token):

    global RDP_HOST

    app_key_bytes = app_key.encode('ascii')
    base64_bytes = base64.b64encode(app_key_bytes)
    app_key_base64 = base64_bytes.decode('ascii')

    auth_url = f'{RDP_HOST}/auth/oauth2/v1/revoke'

    payload = f'token={access_token}'

    try:
        response = requests.post(auth_url,
                                 data = payload,
                                 headers= {
                                     'Content-Type':'application/x-www-form-urlencoded',
                                    'Authorization': f'Basic {app_key_base64}'
                                 },
                                 auth=(app_key, ''))
    except requests.exceptions.RequestException as e:
        print(f'RDP Authentication Revoke exception: {e}')

    if response.status_code == 200:  # HTTP Status 'OK'
        print('Revoke Token success')
    if response.status_code != 200:
        print(f'RDP authentication failure: {response.status_code} {response.reason}')
        print(f'Text: {response.text}')

def get_historical_data(universe, access_token):

    global RDP_HOST
    interval = 'P1W' #weekly
    start_day = '2025-01-01'
    end_day = '2025-02-10'

    # https://api.refinitiv.com/data/historical-pricing/v1/views/interday-summaries/IBM.N
    historical_pricing_url = f'{RDP_HOST}/data/historical-pricing/v1/views/interday-summaries/{universe}'

    payload = {'interval': interval, 
               'count':15,
               'fields':'BID,ASK,OPEN_PRC,HIGH_1,LOW_1,TRDPRC_1,NUM_MOVES,TRNOVR_UNS',
               'start':start_day,
               'end':end_day}

    try:
        response = requests.get(url= historical_pricing_url,
                                headers= {
                                    'Authorization': f'Bearer {access_token}'
                                }, 
                                params= payload,
                                verify=True,
                                 allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f'RDP historical-pricing request exception: {e}')

    if response.status_code == 200:  # HTTP Status 'OK'
        print('This is a Historical Pricing data result from RDP API Call')
        print(response.json())
    if response.status_code != 200:
        print(f'RDP historical-pricing request  failure: {response.status_code} {response.reason}')
        print(f'Text: {response.text}')


if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env.
    username = os.environ['MACHINE_ID'] 
    password = os.environ['PASSWORD'] 
    app_key = os.environ['APP_KEY'] 

    universe = 'IBM.N'

    try:
        print('Sending initial Login request message to RDP')
      
        access_token, refresh_token, expires_in = login_v1(username, password, app_key)

        if access_token:
            print(f'Access Token: {access_token}')
            print(f'Expires in: {expires_in}')
            print(f'Refresh Token: {refresh_token}')
            # code to request data
            
            get_historical_data(universe, access_token)
            
            time.sleep(20)
            print('Sending Logout request message to RDP')
            logout(app_key, access_token)
    except Exception as exp:
        print(f'Exception {exp}')
