# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------

import lseg.data as ld
from lseg.data import session

def get_news_headlines(universe):

    start_day = '2025-01-01'
    end_day = '2025-02-10'

    query = f'R:{universe} AND Language:LEN AND Source:RTRS'

    df = ld.news.get_headlines(query, start=start_day, end=end_day, count=5)

    print('This is a News headlines from Data Library - Access Layer - get_headlines')
    print(df)
    return df

def get_news_story(story_id):

    story = ld.news.get_story(story_id, format=ld.news.Format.TEXT)
    print(f'This is a News story from Data Library - Access Layer - get_story for {story_id}')
    print(story)

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
            headlines = get_news_headlines(universe)
            story_id = headlines.iloc[-1]['storyId']
            print()
            get_news_story(story_id)

        print('Close Session')
        session.close()
        ld.close_session()
    except Exception as exp:
        print(f'Exception {exp}')
