# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------

import lseg.data as ld
from lseg.data.content import esg
from lseg.data import session

def get_esg_standard(universe):

    response = esg.standard_scores.Definition(universe).get_data()

    print('This is an ESG data result from Data Library - Content Layer - esg.standard_scores')
    # print raw data 
    #print(response.data)
    print(response.data.df)

if __name__ == '__main__':
    universe = 'IBM.N'

    try:
        print('Open Session')
        # Open the data session
        ld.open_session()
        #ld.open_session(config_name='./lseg-data.devrel.config.json')
        session = ld.session.Definition().get_session()
        session.open()

        # code to request data
        if str(session.open_state) == 'OpenState.Opened':
            get_esg_standard(universe)

        print('Close Session')
        ld.close_session()
    except Exception as exp:
        print(f'Exception {exp}')
