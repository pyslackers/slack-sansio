import os
import sys
import pprint
import logging

import requests
import slack
from slack.io.requests import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def iterate(client):

    for channel in client.iter(slack.methods.CHANNELS_LIST, limit=2):
        pprint.pprint(channel)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get("SLACK_TOKEN")

    if not TOKEN:
        raise ValueError("No slack token provided !")

    session = requests.session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    iterate(slack_client)
