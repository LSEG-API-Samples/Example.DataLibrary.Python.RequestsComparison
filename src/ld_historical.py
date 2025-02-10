# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------

import lseg.data as ld
from lseg.data import session

def get_historical_data(universe, fields):
    # Time Variables
    interval = 'weekly' #weekly
    start_day = '2025-01-01'
    end_day = '2025-02-10'

    df = ld.get_history(universe=universe,
                        interval=interval, 
                        fields=fields,
                        count=15,
                        start=start_day,
                        end= end_day)
    print('This is a Historical Pricing data result from Data Library - get_history() method')
    print(df)

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
            get_historical_data(universe, fields)

        print('Close Session')
        session.close()
        ld.close_session()
    except Exception as exp:
        print(f'Exception {exp}')
