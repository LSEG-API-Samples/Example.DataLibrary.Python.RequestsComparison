# Comparison of Data Library for Python VS Python/requests direct call for the Delivery Platform (RDP)
- version: 1.0
- Last update: February 2025
- Environment: Windows
- Compiler: Python

## <a id="data_library_intro"></a>Introduction to Data Library

The Data Library provides a set of ease-of-use interfaces offering coders uniform access to the breadth and depth of financial data and services available on the LSEG Data Platform. The Library is designed to provide consistent access through multiple access channels and target both Professional Developers and Financial Coders.

![figure-1](images/data_library_1.png "Data Library access points")

The library is available the following programming languages

- [Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python)
- [.NET](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-net)
- [TypeScript](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-library-for-typescript)

Once connected, applications can rely on easy-to-use objects and functions to access the breadth and depth of data services available on the platform. Or alternatively, applications can use service-agnostic lower layer, that enable an access to the fine-grained details of each platform service. 

![figure-2](images/data_library_2.png "Data Library concept")

### Data Library Abstraction Layers

Depending on the skill and comfort level of the developer, the library offers various of API interface layers from high-level Access Layer, medium-level Content Layer, and a low-level Delivery Layer that suit different types of developers. 

![figure-2](images/lseg-data-libraries-layers.png "Data Library Layers")

**Note**:
- This project demonstrates with the LSEG Data Library for Python which is the version 2.0.1 of the library (**As of February 2025**)
- For High performance scenarios, the Real-Time SDK ([C++](https://developers.lseg.com/en/api-catalog/real-time-opnsrc/rt-sdk-cc), [Java](https://developers.lseg.com/en/api-catalog/real-time-opnsrc/rt-sdk-java), [C#](https://developers.lseg.com/en/api-catalog/real-time-opnsrc/rt-sdk-csharp)) and [Real-Time WebSocket API](https://developers.lseg.com/en/api-catalog/real-time-opnsrc/websocket-api) are recommended

## <a id="authen"></a>Initialize and Authentication

RDP APIs entitlement check is based on OAuth 2.0 specification. The first step of an application work flow is to get a token, which will allow access to the protected resource, i.e. data REST API's.  The RDP currently supports two version of Authentication methods (**As of February 2025**).

Both RDP APIs and Data Library PlatformSession applications require the RDP access credential and login process to get data from the platform.

### Authentication Version 1 - Initial Login

The API endpoint **https://api.refinitiv.com/auth/oauth2/v1/token** (please be noticed **v1**) requires the following access credential information:

- Username: The username. 
- Password: Password associated with the username. .
- Client ID: This is also known as ```AppKey```, and it is generated using an Appkey Generator. This unique identifier is defined for the user or application and is deemed confidential (not shared between users).
-  Grant Type **password**

#### Direct RDP APIs call with Python/requests

The application needs to send a HTTP Post message with the access credentials to RDP Auth Service endpoint URL (V1). 

A successful authentication response message from RDP Auth Service contains the following parameters:

- **access_token**: The token used to invoke REST data API calls as described above. The application must keep this credential for further RDP/Real-Time - Optimized requests.
- **refresh_token**: Refresh token to be used for obtaining an updated access token before expiration. The application must keep this credential for access token renewal.
- **expires_in**: Access token validity time in seconds.
- **scope**: A list of all the scopes this token can be used with.

For the full detail and explanation of RDP Authentication process application workflow, please refer to the following RDP APIS tutorials:

- [Introduction to the Request-Response API](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api).
- [Authorization - All about tokens](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens).
- [Authorization in Python](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-in-python).

Example Code with Python request library (see ```requests_session_v1.py``` file):

```python

import requests

RDP_HOST = 'https://api.refinitiv.com'

auth_url = f'{RDP_HOST}/auth/oauth2/v1/token'
scope = 'trapi'

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
# Handle Errors

```

The above code is very straightforward, the application creates an authentication request message in JSON message format, send HTTP Post request message and get authentication result if HTTP status response is 200 (Ok).  Please note that it is mandatory to keep the access token, refresh token, and expires_in values for later use.

However, the Data Library gives developers the easiest way to authenticates with RDP Auth Service.

#### Data Library

With Data Library, developers can configure the RDP access credential in a configuration file name ```lseg-data.config.json``` as follows:


```json
{
    "sessions": {
        "default": "platform.ldp",
        "platform": {
            "ldp": {
                "app-key": "YOUR APP KEY GOES HERE!",
                "username": "YOUR LDP LOGIN OR MACHINE GOES HERE!",
                "password": "YOUR LDP PASSWORD GOES HERE!",
                "signon_control":true
            }
        }
    }
}
```

The file must be located on a running directory of an application. Then uses the following code to open a connection with the platform.

Example Code (see ```ld_session.py``` file)

```python
import lseg.data as ld

# Open the data session
ld.open_session()

# request data
```

That is all the code the Data Library application needs to call to login and connect to the RDP platform. An application also does not need to manage the access token, refresh token and expires_in values as the Library manages them for an application.

An application can also use the Library's Session Layer to get the status of a connection as follows:

```python
import lseg.data as ld
from lseg.data import session

# Open the data session
ld.open_session()
session = ld.session.Definition().get_session()
session.open()
if str(session.open_state) == 'OpenState.Opened': # Session is opened successfully

# code to request data

```

Please note that developers can choose to pass an access credential to the Library function directly too. Please see more detail on the [GitHub](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python/tree/lseg-data-examples/Examples/4-Session) repository.

### Authentication Version 1 - Refresh Login

Before the session expires (based on the ```expires_in``` parameter, in seconds) , an application needs to send a Refresh Grant request message to RDP Authentication service (**https://api.refinitiv.com/auth/oauth2/v1/token** URL) to get a new access token before further request data from the platform.

The API requires the following access credential information:

- Refresh Token: The current Refresh Token value from the previous RDP Authentication call
- Client ID: This is also known as AppKey, and it is generated using an App key Generator. 
- Grant Type **refresh_token**: This is for getting a new Access Token.

Once the refresh token process is succeed, an application gets ```access_token```, ```refresh_token```, and ```expires_in``` from the RDP Auth service response message the same as an initial Login RDP Authentication call. An application must keep those value for the next Refresh Token call.

#### Direct RDP APIs call with Python/requests

The code can send a refresh grant request message to the RDP Authentication Service Endpoint (V1) the same way as an initial login request.

```python
auth_url = f'{RDP_HOST}/auth/oauth2/v1/token'

# For the Refresh Grant scenario
payload=f'grant_type=refresh_token&client_id={app_key}&refresh_token={refresh_token}'

try:
    response = requests.post(auth_url, 
                                data=payload, 
                                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                verify=True,
                                allow_redirects=False)
except requests.exceptions.RequestException as e:
    print(f'RDP Authentication Refresh Token exception: {e}')
    return None, None, None
```

Even though the code is the almost same as an initial login request message, an application has a responsibility to manage and handle an ```expires_in``` value.

#### Data Library

With the Data Library, the library automatic maintains the RDP session under the hood for an application as long as an application does not call the close session method explicitly. 

### Authentication Version 1 - Revoke Login

This revocation mechanism allows an application to invalidate its tokens if the end-user logs out, changes identity, or exits the respective application. Notifying the authorization server that the token is no longer needed allows the authorization server to clean up data associated with that token (e.g., session data) and the underlying authorization grant.

#### Direct RDP APIs call with Python/requests

The code can send a HTTP request message to **https://api.refinitiv.com/auth/oauth2/v1/revoke** with the following condition in order to revoke the current access token.

- HTTP Header: 
    * Authorization = ```Basic <App Key in Base64 format>```
Please notice *the space* between the ```Basic``` and ```App Key in Base64 format``` values.

- Body parameter
    * token: The current ```Access Token``` value from the previous RDP Authentication call

Example Code:

```python
import base64

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
```

Now, let's see how the Data Library close a session.

#### Data Library

An application can just call a single library method to close a connection as follows:

```python
import lseg.data as ld

# Open Session

# Close Default Session
ld.close_session()
```

### Authentication Version 2

The API endpoint **https://api.refinitiv.com/auth/oauth2/v2/token** (please be noticed **v2**) requires the following access credential information:

- client_id ID: The Service ID (aks Service User). 
- client_secret: Password associated with the Service user.
- Grant Type **client_credentials**
- scope (optional): Limits the scope of the generated token so that the Access token is valid only for a specific data set

**Note**: The ```V2 client_id``` **is not the same value** as the ```V1 client_id```. The ```V1 client_id``` is an ```app key``` of the [V1 - Password Grant Model](https://www.oauth.com/oauth2-servers/access-tokens/password-grant/).

[tbd]