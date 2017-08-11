import os
import sys
import pprint
import asyncio
import aiohttp
import logging

from slack.io.aiohttp import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

async def query(client):

    data = await client.query('auth.test')
    pprint.pprint(data)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get('SLACK_TOKEN')

    if not TOKEN:
        raise ValueError('No slack token provided !')

    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    slack_client = SlackAPI(token=TOKEN, session=session)

    try:
        loop.run_until_complete(query(slack_client))
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(session.close())
