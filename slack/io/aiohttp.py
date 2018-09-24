import asyncio
from typing import Tuple, Union, Optional, AsyncIterator, MutableMapping

import aiohttp

from . import abc
from .. import methods


class SlackAPI(abc.SlackAPI):
    """
    `aiohttp` implementation of :class:`slack.io.abc.SlackAPI`

    Args:
        session: HTTP session
    """

    def __init__(self, *, session: aiohttp.ClientSession, **kwargs) -> None:
        self._session = session
        super().__init__(**kwargs)

    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[MutableMapping],
        body: Optional[Union[str, MutableMapping]],
    ) -> Tuple[int, bytes, MutableMapping]:
        async with self._session.request(
            method, url, headers=headers, data=body
        ) as response:
            return response.status, await response.read(), response.headers

    async def _rtm(self, url: str) -> AsyncIterator[str]:

        async with self._session.ws_connect(url) as ws:
            async for data in ws:
                if data.type == aiohttp.WSMsgType.TEXT:
                    yield data.data
                elif data.type == aiohttp.WSMsgType.CLOSED:
                    break
                elif data.type == aiohttp.WSMsgType.ERROR:
                    break

    async def sleep(self, seconds: Union[int, float]) -> None:
        await asyncio.sleep(seconds)
