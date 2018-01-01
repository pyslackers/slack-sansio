import curio

from . import abc


class SlackAPI(abc.SlackAPI):
    """
    `asks curio` implementation of :class:`slack.io.abc.SlackAPI`

    Args:
        session: HTTP session
    """
    def __init__(self, *, session, **kwargs):
        self._session = session
        super().__init__(**kwargs)

    async def _request(self, method, url, headers, body):
        response = await self._session.request(method, url, headers=headers, data=body)
        return response.status_code, response.content, response.headers

    async def rtm(self, url=None, bot_id=None):
        raise NotImplementedError

    async def _rtm(self, url):
        raise NotImplementedError

    async def sleep(self, seconds):
        await curio.sleep(seconds)
