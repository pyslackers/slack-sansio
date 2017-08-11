import abc
import json
import time
import logging

from .. import sansio, exceptions
from ..events import Event, Message

LOG = logging.getLogger(__name__)


class SlackAPI(abc.ABC):

    def __init__(self, *, session, token, raise_on_rate_limit=False, headers=None):
        self._session = session
        self._token = token
        self._headers = headers or {}
        self._raise_on_rate_limit = raise_on_rate_limit
        self._rate_limited = False

    @abc.abstractmethod
    async def _request(self, method, url, headers, body):
        """Make the http request"""

        return '', {}, b''

    @abc.abstractmethod
    async def _rtm(self, url):
        pass

    @abc.abstractmethod
    async def sleep(self, seconds):
        pass

    async def _make_query(self, url, data=None, headers=None):

        while self._rate_limited and self._rate_limited > int(time.time()):
            await self.sleep(1)

        try:
            url, body, headers = sansio.prepare_request(url=url, data=data, headers=headers,
                                                        global_headers=self._headers, token=self._token)
            status, body, headers = await self._request('POST', url, headers, body)
            response_data = sansio.decode_request(status, headers, body)
        except exceptions.RateLimited as rate_limited:
            if self._raise_on_rate_limit:
                raise
            else:
                LOG.warning('Rate limited ! Waiting for %s seconds', rate_limited.retry_after)
                self._rate_limited = int(time.time()) + rate_limited.retry_after
                return await self._make_query(url, data, headers)
        else:
            self._rate_limited = False
            return response_data

    async def query(self, url, data=None, headers=None):

        if isinstance(data, Message):
            data = data.serialize()

        return await self._make_query(url, data, headers)

    async def iter(self, url, data=None, headers=None, *, limit=200, iterkey=None, itermode=None, itervalue=None):
        while True:
            data, iterkey, itermode = sansio.prepare_iter_request(url, data, iterkey=iterkey, itermode=itermode,
                                                                  limit=limit, itervalue=itervalue)
            response_data = await self._make_query(url, data, headers)
            itervalue = sansio.decode_iter_request(response_data)
            for item in response_data[iterkey]:
                yield item

            if not itervalue:
                break

    async def rtm(self, url=None, bot_id=None):
        while True:
            if not bot_id:
                auth = await self.query('auth.test')
                user_info = await self.query('users.info', {'user': auth['user_id']})
                bot_id = user_info['user']['profile']['bot_id']
                LOG.info('BOT_ID is %s', bot_id)
            if not url:
                url = (await self.query('rtm.connect'))['url']

            async for data in self._rtm(url):
                event = Event.from_rtm(json.loads(data))
                if sansio.need_reconnect(event):
                    break
                elif sansio.discard_event(event, bot_id):
                    if event['type'] == 'reconnect_url':
                        url = event['url']
                else:
                    yield event
