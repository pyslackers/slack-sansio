import os
import sys
import asks
import slack
import curio
import pprint
import logging

from slack.io.curio import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

asks.init('curio')


async def query(client):

    data = await client.query(slack.methods.AUTH_TEST)
    pprint.pprint(data)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get('SLACK_TOKEN')

    if not TOKEN:
        raise ValueError('No slack token provided !')

    session = asks.Session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    curio.run(query(slack_client))
