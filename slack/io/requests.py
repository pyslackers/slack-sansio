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

    Args:
        session: HTTP session
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

    def _make_query(self, url, body, headers):

        while self.rate_limited and self.rate_limited > int(time.time()):
            self.sleep(self.rate_limited - int(time.time()))

        status, rep_body, rep_headers = self._request('POST', url, headers, body)

        try:
            response_data = sansio.decode_response(status, rep_headers, rep_body)
        except exceptions.RateLimited as rate_limited:
            if self._retry_when_rate_limit:
                LOG.warning('Rate limited ! Waiting for %s seconds', rate_limited.retry_after)
                self.rate_limited = int(time.time()) + rate_limited.retry_after
                return self._make_query(url, body, headers)
            else:
                raise
        else:
            self.rate_limited = False
            return response_data

    def query(self, url, data=None, headers=None, as_json=None):
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
        url, body, headers = sansio.prepare_request(url=url, data=data, headers=headers,
                                                    global_headers=self._headers, token=self._token)
        return self._make_query(url, body, headers)

    def iter(self, url, data=None, headers=None, *, limit=200, iterkey=None, itermode=None, minimum_time=None,
             as_json=None):
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
            if minimum_time and last_request_time and last_request_time + minimum_time > current_time:
                self.sleep(last_request_time + minimum_time - current_time)

            data, iterkey, itermode = sansio.prepare_iter_request(url, data, iterkey=iterkey, itermode=itermode,
                                                                  limit=limit, itervalue=itervalue)
            last_request_time = time.time()
            response_data = self.query(url, data, headers, as_json)
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
            bot_id = bot_id or self._find_bot_id()
            url = url or self._find_rtm_url()
            for event in self._incoming_from_rtm(url, bot_id):
                yield event
            url = None

    def _find_bot_id(self):
        auth = self.query(methods.AUTH_TEST)
        user_info = self.query(methods.USERS_INFO, {'user': auth['user_id']})
        bot_id = user_info['user']['profile']['bot_id']
        LOG.info('BOT_ID is %s', bot_id)
        return bot_id

    def _find_rtm_url(self):
        response = self.query(methods.RTM_CONNECT)
        return response['url']

    def _incoming_from_rtm(self, url, bot_id):
        for data in self._rtm(url):
            event = events.Event.from_rtm(json.loads(data))
            if sansio.need_reconnect(event):
                break
            elif sansio.discard_event(event, bot_id):
                continue
            else:
                yield event
