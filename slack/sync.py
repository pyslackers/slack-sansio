import requests

from . import abc


class SlackAPI(abc.SlackAPI):

    def _request(self, method, url, headers, body):

        response = requests.request(method, url, headers=headers, data=body)
        return response.status_code, response.headers, response.content

