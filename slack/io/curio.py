from typing import Tuple, Union, Optional, AsyncIterator, MutableMapping

import asks
import curio

from . import abc


class SlackAPI(abc.SlackAPI):
    """
    `asks curio` implementation of :class:`slack.io.abc.SlackAPI`

    Args:
        session: HTTP session
    """

    def __init__(self, *, session: asks.Session, **kwargs) -> None:
        self._session = session
        super().__init__(**kwargs)

    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[MutableMapping],
        body: Optional[Union[str, MutableMapping]],
    ) -> Tuple[int, bytes, MutableMapping]:

        response = await self._session.request(method, url, headers=headers, data=body)
        return response.status_code, response.content, response.headers

    async def rtm(self, url=None, bot_id=None):
        raise NotImplementedError

    async def _rtm(self, url: str) -> AsyncIterator[str]:
        yield ""
        raise NotImplementedError

    async def sleep(self, seconds: float) -> None:
        await curio.sleep(seconds)
