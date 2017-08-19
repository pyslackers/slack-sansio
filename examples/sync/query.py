import os
import sys
import pprint
import logging
import requests
import slack

from slack.io.sync import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def query(client):
    data = client.query(slack.methods.AUTH_TEST)
    pprint.pprint(data)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get('SLACK_TOKEN')

    if not TOKEN:
        raise ValueError('No slack token provided !')

    session = requests.session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    query(slack_client)
