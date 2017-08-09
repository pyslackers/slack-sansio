import requests

from . import abc


class SlackAPI(abc.SlackAPI):

    def _request(self, method, url, headers, body):

        response = requests.request(method, url, headers=headers, data=body)
        return response.status_code, response.headers, response.content

    def post(self, url, data=None):
        data = data or {}
        url, headers, body = self._pre_request(url, data)
        status, headers, body = self._request('POST', url, headers, body)
        data = self._post_request(status, headers, body)
        return data
