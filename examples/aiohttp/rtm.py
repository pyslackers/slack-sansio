import os
import sys
import pprint
import asyncio
import aiohttp
import logging
import slack

from slack.io.aiohttp import SlackAPI
from slack.events import Message

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

async def rtm(client):

    async for event in client.rtm():
        pprint.pprint(event)

        if isinstance(event, Message):
            asyncio.ensure_future(respond_to_message(event, client))

async def respond_to_message(message, client):
    response = message.response()
    response['text'] = 'Hello world !'
    await client.query(slack.methods.CHAT_POST_MESSAGE, data=response.serialize())

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
        loop.run_until_complete(rtm(slack_client))
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(session.close())
