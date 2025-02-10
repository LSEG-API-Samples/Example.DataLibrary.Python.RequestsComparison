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

def get_news_headlines(universe, access_token):

    global RDP_HOST

    # https://api.refinitiv.com/data/news/v1/headlines?query={{query}}
    headlines_url = f'{RDP_HOST}/data/news/v1/headlines'
    payload = {'query': f'R:{universe} AND Language:LEN AND Source:RTRS','limit':5}

    try:
        response = requests.get(url= headlines_url,
                                headers= {
                                    'Authorization': f'Bearer {access_token}'
                                }, 
                                params= payload,
                                verify=True,
                                 allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f'RDP ESG request exception: {e}')

    if response.status_code == 200:  # HTTP Status 'OK'
        print('This is an News headlines result from RDP API Call')
        print(response.json())
        return response.json()
    if response.status_code != 200:
        print(f'RDP News request  failure: {response.status_code} {response.reason}')
        print(f'Text: {response.text}')

def get_news_story(story_id, access_token):

    global RDP_HOST

    # https://api.refinitiv.com/data/news/v1/stories/{{story_id}}
    story_url = f'{RDP_HOST}/data/news/v1/stories/{story_id}'

    try:
        response = requests.get(url= story_url,
                                headers= {
                                    'Authorization': f'Bearer {access_token}'
                                }, 
                                verify=True,
                                 allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f'RDP ESG request exception: {e}')

    if response.status_code == 200:  # HTTP Status 'OK'
        print(f'This is an News story result from RDP API Call for {story_id}')
        print(response.json())
    if response.status_code != 200:
        print(f'RDP News request  failure: {response.status_code} {response.reason}')
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
            #print(f'Access Token: {access_token}')
            print(f'Expires in: {expires_in}')
            #print(f'Refresh Token: {refresh_token}')
            # code to request data
            
            headlines = get_news_headlines(universe, access_token)
            story_id = headlines['data'][-1]['storyId']
            print()
            get_news_story(story_id, access_token)
            
            time.sleep(20)
            print('Sending Logout request message to RDP')
            logout(app_key, access_token)
    except Exception as exp:
        print(f'Exception {exp}')
