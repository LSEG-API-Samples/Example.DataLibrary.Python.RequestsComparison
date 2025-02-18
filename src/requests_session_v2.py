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


def login_v2(client_id, client_secret):
    """
    This method sends a HTTP login request message to RDP Authentication Service V2.

    Args:
        client_id (str): The RDP Client-ID (Service ID)
        client_secret (str): The RDP Client-Secret

     Returns: 
        access token (str): The Access Token
        expires_in (int): The expires_in value
    """
    global RDP_HOST
    if not client_secret or not client_id:
        raise TypeError('Missing required parameters')

    auth_url = f'{RDP_HOST}/auth/oauth2/v2/token'

    payload=f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scope={scope}'

    # Send HTTP request
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
        return response.json()['access_token'],  int(response.json()['expires_in'])
    if response.status_code != 200:
        print(f'RDP authentication failure: {response.status_code} {response.reason}')
        print(f'Text: {response.text}')
        raise requests.exceptions.HTTPError(f'RDP authentication failure: {response.status_code} - {response.text} ', response = response )
    

if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env.
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    try:
        print('Sending initial Login request message to RDP')
        access_token, expires_in = login_v2(client_id, client_secret)
        if access_token:
            print(f'Access Token: {access_token}')
            print(f'Expires in: {expires_in}')
            # code to request data
            
            time.sleep(20)
            print('Sending re-Login request message to RDP')
            access_token, expires_in = login_v2(client_id, client_secret)
            print(f'New Access Token: {access_token}')
            time.sleep(10)
            print('Authentication Version 2 does not need to revoke :)')
    except Exception as exp:
        print(f'Exception {exp}')

        

    
        
