# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------

import lseg.data as ld
from lseg.data import session
from lseg.data.delivery import endpoint_request

def get_analytics_working_day(codes, date):
    """
    This method sends a request message to RDP Analytics service with the Data Library Endpoint object and print data on a console.

    Args:
        codes (list of str): List of Country Codes
        date (str): The date data in YYYY-MM-DD format

    Returns: 
        None
    """

    analytic_url = 'https://api.refinitiv.com/analytics/functions/v1/common/is-working-day'

    payload = {
        'universe': [{
                'calendarCodes': codes,
                'calculationDate': date
            }]
        }

    # Create request object
    request = ld.delivery.endpoint_request.Definition(
        url = analytic_url,
        method= ld.delivery.endpoint_request.RequestMethod.POST,
        body_parameters= payload
    )
    # Send HTTP request
    response = request.get_data()
    print('This is a IS-Working-Day data result from Data Library - Delivery Layer - Endpoint method')
    print(response.data.raw)

def get_historical_event(universe):
    """
    This method sends a request message to RDP Historical Pricing service with the Data Library Endpoint object and print data on a console.

    Args:
        universe (str): RIC Code

    Returns: 
        None
    """
    historical_url = 'https://api.refinitiv.com/data/historical-pricing/v1/views/events/{universe}'

    # Create request object
    request = ld.delivery.endpoint_request.Definition(
        url = historical_url,
        method= ld.delivery.endpoint_request.RequestMethod.GET,
        path_parameters={'universe':universe},
        body_parameters= {
        'eventTypes': 'trade,correction',
        'adjustments': 'exchangeCorrection,manualCorrection'
    }
    )
    # Send HTTP request
    response = request.get_data()
    print('This is a Historical Pricing Event data result from Data Library - Delivery Layer - Endpoint method')
    print(response.data.raw)

if __name__ == '__main__':
    country_codes = ['THA']
    universe = 'IBM.N'
    day='2025-02-12'
    try:
        print('Open Session')
        # Open the data session
        ld.open_session()
        #ld.open_session(config_name='./lseg-data.devrel.config.json')
        session = ld.session.Definition().get_session()
        session.open()

        # code to request data
        if str(session.open_state) == 'OpenState.Opened':
            get_analytics_working_day(country_codes, day)
            print()
            get_historical_event(universe)

        print('Close Session')
        ld.close_session()
    except Exception as exp:
        print(f'Exception {exp}')