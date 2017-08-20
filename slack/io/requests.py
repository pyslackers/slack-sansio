import time
import json
import logging
import websocket

from . import abc
from .. import sansio, exceptions, events, methods

LOG = logging.getLogger(__name__)


class SlackAPI(abc.SlackAPI):
    """
    `requests` implementation of :class:`slack.io.abc.SlackAPI`
    """

    def __init__(self, *, session, **kwargs):
        self._session = session
        super().__init__(**kwargs)

    def _request(self, method, url, headers, body):

        response = self._session.request(method, url, headers=headers, data=body)
        return response.status_code, response.content, response.headers

    def _rtm(self, url):

        ws = websocket.create_connection(url)
        while True:
            event = ws.recv()
            if event:
                yield event
            else:
                self.sleep(0.5)

    def sleep(self, seconds):
        time.sleep(seconds)

    def _make_query(self, url, data=None, headers=None):

        while self._rate_limited and self._rate_limited > int(time.time()):
            self.sleep(1)

        try:
            url, body, headers = sansio.prepare_request(url=url, data=data, headers=headers,
                                                        global_headers=self._headers, token=self._token)
            status, body, headers = self._request('POST', url, headers, body)
            response_data = sansio.decode_response(status, headers, body)
        except exceptions.RateLimited as rate_limited:
            if self._retry_when_rate_limit:
                raise
            else:
                LOG.warning('Rate limited ! Waiting for %s seconds', rate_limited.retry_after)
                self._rate_limited = int(time.time()) + rate_limited.retry_after
                return self._make_query(url, data, headers)
        else:
            self._rate_limited = False
            return response_data

    def query(self, url, data=None, headers=None):
        """
        Query the slack API

        Args:
            url: :class:`slack.methods` or url string
            data: JSON encodable MutableMapping
            headers: Custom headers

        Returns:
            dictionary of slack API response data

        """
        return self._make_query(url, data, headers)

    def iter(self, url, data=None, headers=None, *, limit=200, iterkey=None, itermode=None):
        """
        Iterate over a slack API method supporting pagination

        Args:
            url: :class:`slack.methods` or url string
            data: JSON encodable MutableMapping
            headers:
            limit: Maximum number of results to return per call.
            iterkey: Key in response data to iterate over (required for url string).
            itermode: Iteration mode (required for url string) (one of `cursor`, `page` or `timeline`)

        Returns:
            Async iterator over `response_data[key]`

        """
        itervalue = None
        while True:
            data, iterkey, itermode = sansio.prepare_iter_request(url, data, iterkey=iterkey, itermode=itermode,
                                                                  limit=limit, itervalue=itervalue)
            response_data = self._make_query(url, data, headers)
            itervalue = sansio.decode_iter_request(response_data)
            for item in response_data[iterkey]:
                yield item

            if not itervalue:
                break

    def rtm(self, url=None, bot_id=None):
        """
        Iterate over event from the RTM API

        Args:
            url: Websocket connection url
            bot_id: Connecting bot ID

        Returns:
            :class:`slack.events.Event` or :class:`slack.events.Message`

        """
        while True:
            if not bot_id:
                auth = self.query(methods.AUTH_TEST)
                user_info = self.query(methods.USERS_INFO, {'user': auth['user_id']})
                bot_id = user_info['user']['profile']['bot_id']
                LOG.info('BOT_ID is %s', bot_id)
            if not url:
                url = (self.query(methods.RTM_CONNECT))['url']

            for data in self._rtm(url):
                event = events.Event.from_rtm(json.loads(data))
                if sansio.need_reconnect(event):
                    break
                elif sansio.discard_event(event, bot_id):
                    if event['type'] == 'reconnect_url':
                        url = event['url']
                else:
                    yield event
