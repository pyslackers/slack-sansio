import sys
import asyncio
import aiohttp
import pprint

from slack.aiohttp import SlackAPI as aiohttpSlackAPI
from slack.sync import SlackAPI as syncSlackAPI


async def test_aiohttp(loop):
    session = aiohttp.ClientSession(loop=loop)
    slack = aiohttpSlackAPI(
        session=session,
        token=sys.argv[1]
    )

    async for user in slack.postiter('users.list', limit=10):
        pprint.pprint(user)


def test_sync():

    slack = syncSlackAPI(token=sys.argv[1])
    for user in slack.postiter('users.list', limit=10):
        pprint.pprint(user)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_aiohttp(loop))
    # print('*****' * 50)
    test_sync()
