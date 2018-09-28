import json
import time
import logging
from typing import Tuple, Union, Optional, AsyncIterator, MutableMapping

from .. import events, sansio, methods, exceptions

LOG = logging.getLogger(__name__)


class SlackAPI:
    """
    :py:term:`abstract base class` abstracting the HTTP library used to call Slack API. Built with the functions of
    :mod:`slack.sansio`.

    Args:
        session: HTTP session
        token: Slack API token
        headers: Default headers for all request
    """

    def __init__(self, *, token: str, headers: Optional[MutableMapping] = None) -> None:
        self._token = token
        self._headers = headers or {}

    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[MutableMapping],
        body: Optional[Union[str, MutableMapping]],
    ) -> Tuple[int, bytes, MutableMapping]:
        raise NotImplementedError()

    async def _rtm(self, url: str) -> AsyncIterator[str]:
        yield ""
        raise NotImplementedError()

    async def sleep(self, seconds: Union[int, float]):
        raise NotImplementedError()

    async def _make_query(
        self,
        url: str,
        body: Optional[Union[str, MutableMapping]],
        headers: Optional[MutableMapping],
    ) -> dict:

        LOG.debug("Querying %s with %s, %s", url, headers, body)
        status, rep_body, rep_headers = await self._request("POST", url, headers, body)
        LOG.debug("Response from %s: %s, %s, %s", url, status, rep_body, rep_headers)

        response_data = sansio.decode_response(status, rep_headers, rep_body)
        return response_data

    async def query(
        self,
        url: Union[str, methods],
        data: Optional[MutableMapping] = None,
        headers: Optional[MutableMapping] = None,
        as_json: Optional[bool] = None,
    ) -> dict:
        """
        Query the slack API

        When using :class:`slack.methods` the request is made `as_json` if available

        Args:
            url: :class:`slack.methods` or url string
            data: JSON encodable MutableMapping
            headers: Custom headers
            as_json: Post JSON to the slack API
        Returns:
            dictionary of slack API response data

        """

        url, body, headers = sansio.prepare_request(
            url=url,
            data=data,
            headers=headers,
            as_json=as_json,
            global_headers=self._headers,
            token=self._token,
        )
        return await self._make_query(url, body, headers)

    async def iter(
        self,
        url: Union[str, methods],
        data: Optional[MutableMapping] = None,
        headers: Optional[MutableMapping] = None,
        *,
        limit: int = 200,
        iterkey: Optional[str] = None,
        itermode: Optional[str] = None,
        minimum_time: Optional[int] = None,
        as_json: Optional[bool] = None
    ) -> AsyncIterator[dict]:
        """
        Iterate over a slack API method supporting pagination

        When using :class:`slack.methods` the request is made `as_json` if available

        Args:
            url: :class:`slack.methods` or url string
            data: JSON encodable MutableMapping
            headers:
            limit: Maximum number of results to return per call.
            iterkey: Key in response data to iterate over (required for url string).
            itermode: Iteration mode (required for url string) (one of `cursor`, `page` or `timeline`)
            minimum_time: Minimum elapsed time (in seconds) between two calls to the Slack API (default to 0).
             If not reached the client will sleep for the remaining time.
            as_json: Post JSON to the slack API
        Returns:
            Async iterator over `response_data[key]`

        """
        itervalue = None

        if not data:
            data = {}

        last_request_time = None
        while True:
            current_time = time.time()
            if (
                minimum_time
                and last_request_time
                and last_request_time + minimum_time > current_time
            ):
                await self.sleep(last_request_time + minimum_time - current_time)

            data, iterkey, itermode = sansio.prepare_iter_request(
                url,
                data,
                iterkey=iterkey,
                itermode=itermode,
                limit=limit,
                itervalue=itervalue,
            )
            last_request_time = time.time()
            response_data = await self.query(url, data, headers, as_json)
            itervalue = sansio.decode_iter_request(response_data)
            for item in response_data[iterkey]:
                yield item

            if not itervalue:
                break

    async def rtm(
        self, url: Optional[str] = None, bot_id: Optional[str] = None
    ) -> AsyncIterator[events.Event]:
        """
        Iterate over event from the RTM API

        Args:
            url: Websocket connection url
            bot_id: Connecting bot ID

        Returns:
            :class:`slack.events.Event` or :class:`slack.events.Message`

        """
        while True:
            bot_id = bot_id or await self._find_bot_id()
            url = url or await self._find_rtm_url()
            async for event in self._incoming_from_rtm(url, bot_id):
                yield event
            url = None

    async def _find_bot_id(self) -> str:
        """
        Find the bot ID to discard incoming message from the bot itself.

        Returns:
            The bot ID
        """
        auth = await self.query(methods.AUTH_TEST)
        user_info = await self.query(methods.USERS_INFO, {"user": auth["user_id"]})
        bot_id = user_info["user"]["profile"]["bot_id"]
        LOG.info("BOT_ID is %s", bot_id)
        return bot_id

    async def _find_rtm_url(self) -> str:
        """
        Call `rtm.connect` to find the websocket url.

        Returns:
            Url for websocket connection
        """
        response = await self.query(methods.RTM_CONNECT)
        return response["url"]

    async def _incoming_from_rtm(
        self, url: str, bot_id: str
    ) -> AsyncIterator[events.Event]:
        """
        Connect and discard incoming RTM event if necessary.

        :param url: Websocket url
        :param bot_id: Bot ID
        :return: Incoming events
        """
        async for data in self._rtm(url):
            event = events.Event.from_rtm(json.loads(data))
            if sansio.need_reconnect(event):
                break
            elif sansio.discard_event(event, bot_id):
                continue
            else:
                yield event
