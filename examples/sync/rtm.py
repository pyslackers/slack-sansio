import os
import sys
import pprint
import logging
import requests

from slack.io.sync import SlackAPI
from slack.events import Message

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def rtm(client):

    for event in client.rtm():
        pprint.pprint(event)

        if isinstance(event, Message):
            respond_to_message(event, client)


def respond_to_message(message, client):
    response = message.response()
    response['text'] = 'Hello world !'
    client.query('chat.postMessage', data=response.serialize())

if __name__ == '__main__':

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get('SLACK_TOKEN')

    if not TOKEN:
        raise ValueError('No slack token provided !')

    session = requests.session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    rtm(slack_client)
