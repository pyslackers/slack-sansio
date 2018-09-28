from typing import Tuple, Union, Optional, AsyncIterator, MutableMapping

import treq
from twisted.internet import defer, reactor
from twisted.web.http_headers import Headers

from . import abc


class SlackAPI(abc.SlackAPI):
    """
    `treq` implementation of :class:`slack.io.abc.SlackAPI`
    """

    def __init__(self, *args, **kwargs):
        self._reactor = reactor
        super().__init__(*args, **kwargs)

    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[MutableMapping],
        body: Optional[Union[str, MutableMapping]],
    ) -> Tuple[int, bytes, MutableMapping]:

        if not headers:
            headers = {}

        headers = Headers(
            {
                k.encode("utf-8"): [v.encode("utf-8")]
                for k, v in headers.items()
                if k.lower() != "content-length"
            }
        )

        response = await treq.request(method, url, headers=headers, data=body)

        response_headers = {
            k.decode("utf-8").lower(): v[0].decode("utf-8")
            for k, v in response.headers.getAllRawHeaders()
        }

        return response.code, await response.content(), response_headers

    async def rtm(self, url=None, bot_id=None):
        raise NotImplementedError

    async def _rtm(self, url: str) -> AsyncIterator[str]:
        yield ""
        raise NotImplementedError

    async def sleep(self, seconds: float) -> None:
        d = defer.Deferred()
        self._reactor.callLater(seconds, d.callback, None)
        await d
