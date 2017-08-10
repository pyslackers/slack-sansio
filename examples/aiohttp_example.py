import sys
import pprint
import asyncio
import aiohttp

from slack.io.aiohttp import SlackAPI

async def api(token, session):

    client = SlackAPI(token=token, session=session)
    data = await client.post('auth.test')
    pprint.pprint(data)


async def rtm(token, session):

    client = SlackAPI(token=token, session=session)
    async for msg in client.rtm():
        pprint.pprint(msg)


if __name__ == '__main__':
    TOKEN = sys.argv[1]
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)

    try:
        # loop.run_until_complete(api(TOKEN, session))
        loop.run_until_complete(rtm(TOKEN, session))
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(session.close())
