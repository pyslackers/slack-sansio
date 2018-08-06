import os
import sys
import pprint
import asyncio
import logging

import aiohttp
import slack
from slack.io.aiohttp import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


async def iterate(client):

    async for channel in client.iter(slack.methods.CHANNELS_LIST, limit=4):
        pprint.pprint(channel)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get("SLACK_TOKEN")

    if not TOKEN:
        raise ValueError("No slack token provided !")

    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    slack_client = SlackAPI(token=TOKEN, session=session, raise_on_rate_limit=True)

    try:
        loop.run_until_complete(iterate(slack_client))
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(session.close())
