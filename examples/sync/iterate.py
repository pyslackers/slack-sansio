import os
import sys
import pprint
import logging
import requests

from slack.io.sync import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def iterate(client):

    for channel in client.iter('channels.list', limit=2):
        pprint.pprint(channel)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get('SLACK_TOKEN')

    if not TOKEN:
        raise ValueError('No slack token provided !')

    session = requests.session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    iterate(slack_client)
