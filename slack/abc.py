import cgi
import abc
import json
import logging


from . import HTTPException

LOG = logging.getLogger(__name__)
ROOT_URL = 'https://slack.com/api/'


class SlackAPI(abc.ABC):
    def __init__(self, token):
        self._token = token

    @abc.abstractmethod
    def _request(self, method, url, headers, body):
        """Make the http request"""

        return '', {}, b''

    def _pre_request(self, url, data):
        """Prepare the request"""
        headers = {}
        data['token'] = self._token
        return ROOT_URL + url, headers, data

    def _post_request(self, status, headers, body):
        """Handle the request reponse"""

        content_type = headers.get('content-type')
        type_, parameters = cgi.parse_header(content_type)
        decoded_body = body.decode('utf-8')
        if type_ == 'application/json':
            data = json.loads(decoded_body)
        else:
            data = decoded_body

        if status != 200:
            raise HTTPException(status, data)
        else:
            return data

    def post(self, url, data=None):
        data = data or {}
        url, headers, body = self._pre_request(url, data)
        status, headers, body = self._request('POST', url, headers, body)
        data = self._post_request(status, headers, body)
        return data
