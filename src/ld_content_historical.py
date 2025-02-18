# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------


import lseg.data as ld
from lseg.data.content import historical_pricing
from lseg.data.content.historical_pricing import Intervals
from lseg.data.content.historical_pricing import Adjustments
from lseg.data.content.historical_pricing import EventTypes

def get_historical_interday_data(universe, fields):
    """
    This method sends a request message to RDP Historical Pricing (Interday) service with the DData Library Content Layer and print data on a console.

    Args:
        universe (str): RIC Code
        fields (list of str): List of interested Field names

    Returns: 
        None
    """

    # Send request message
    response = historical_pricing.summaries.Definition(
        universe=universe,
        interval= Intervals.WEEKLY,
        count = 15,
        fields= fields
    ).get_data()
    print('This is a Historical Pricing Inter-Day data result from Data Library - Content Layer - historical_pricing.summaries.Definition method')
    print(response.data.df)

def get_historical_event_data(universe):
    """
    This method sends a request message to RDP Historical Pricing (event) service with the Data Library Content Layer and print data on a console.

    Args:
        universe (str): RIC Code

    Returns: 
        None
    """
    # Send request message
    response = historical_pricing.events.Definition(
        universe=universe,
        eventTypes= [EventTypes.TRADE, EventTypes.CORRECTION],
        adjustments= [
            Adjustments.EXCHANGE_CORRECTION,
            Adjustments.MANUAL_CORRECTION
        ],
        count=15
    ).get_data()

    print('This is a Historical Pricing event data result from Data Library - Content Layer - historical_pricing.summaries.Definition method')
    print(response.data.df)

if __name__ == '__main__':
    universe = 'IBM.N'
    fields=['BID','ASK','OPEN_PRC','HIGH_1','LOW_1','TRDPRC_1','NUM_MOVES','TRNOVR_UNS']
    try:
        print('Open Session')
        # Open the data session
        ld.open_session()
        #ld.open_session(config_name='./lseg-data.devrel.config.json')
        session = ld.session.Definition().get_session()
        session.open()

        # code to request data
        if str(session.open_state) == 'OpenState.Opened':
            get_historical_interday_data(universe, fields)
            print()
            get_historical_event_data(universe)

        print('Close Session')
        ld.close_session()
    except Exception as exp:
        print(f'Exception {exp}')
