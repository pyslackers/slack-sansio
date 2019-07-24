import os
import sys
import pprint
import logging

import asks
import trio
import slack
from slack.io.curio import SlackAPI

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

    session = asks.Session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    trio.run(iterate, slack_client)
