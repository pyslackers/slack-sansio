import abc
import json
import time
import logging
import websocket

from .. import utils

LOG = logging.getLogger(__name__)

ITER_MAPPING = {
    'users.list': 'members'
}


class SlackAPI(abc.ABC):
    def __init__(self, token):
        self._token = token

    @abc.abstractmethod
    def _request(self, method, url, headers, body):
        """Make the http request"""

        return '', {}, b''

    def _pre_request(self, url, data, limit=None, cursor=None, iterkey=None):
        """Prepare the request"""

        headers = {}

        if data:
            data['token'] = self._token
        else:
            data = {'token': self._token}

        if limit:
            data['limit'] = limit

            if cursor:
                data['cursor'] = cursor

        iterkey = iterkey or ITER_MAPPING.get(url)

        if url.startswith('https://hooks.slack.com'):
            body = json.dumps(data)
        elif not url.startswith(utils.ROOT_URL):
            body = data
            url = utils.ROOT_URL + url
        else:
            body = data

        return url, headers, body, iterkey

    def _post_request(self, status, headers, body):
        """Handle the request response"""

        data = utils.decode_body(headers, body)
        utils.raise_for_status(status, data)
        utils.raise_for_api_error(data)

        if 'response_metadata' in data:
            cursor = data['response_metadata'].get('next_cursor')
        else:
            cursor = None

        return data, cursor

    @abc.abstractmethod
    def post(self, url, data=None):

        url, headers, body, *_ = self._pre_request(url, data)
        status, headers, body = self._request('POST', url, headers, body)
        data, *_ = self._post_request(status, headers, body)
        return data

    @abc.abstractmethod
    def postiter(self, url, data=None, limit=200, iterkey=None, cursor=None):

        url, headers, body, iterkey = self._pre_request(
            url, data, limit, cursor, iterkey)
        status, headers, body = self._request('POST', url, headers, body)
        response_data, cursor = self._post_request(status, headers, body)

        for item in response_data[iterkey]:
            yield item

        if cursor:
            yield from self.postiter(url, data, limit, iterkey, cursor)

    @abc.abstractmethod
    def rtm(self):

        data = self.post('rtm.connect')
        ws = websocket.create_connection(data['url'])

        while True:
            msg = ws.recv()
            if msg:
                yield utils.parse_from_rtm(msg)
            else:
                time.sleep(0.1)
