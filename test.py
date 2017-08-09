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

    data = await slack.post('channels.list')
    pprint.pprint(data)


def test_sync():

    slack = syncSlackAPI(token=sys.argv[1])
    data = slack.post('channels.list')
    pprint.pprint(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_aiohttp(loop))
    print('*****' * 50)
    test_sync()
