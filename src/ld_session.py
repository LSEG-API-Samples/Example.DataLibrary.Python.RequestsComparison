# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------

import time
import lseg.data as ld
from lseg.data import session

if __name__ == '__main__':
    try:
        print('Open Session')
        # Open the data session
        ld.open_session()
        #ld.open_session(config_name='./lseg-data.devrel.config.json')
        session = ld.session.Definition().get_session()
        session.open()
        print(f'Session Status: {session.open_state}')
        # code to request data

        time.sleep(20)
        print('Close Session')
        session.close()
        ld.close_session()
    except Exception as exp:
        print(f'Exception {exp}')