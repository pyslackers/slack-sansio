import requests

from . import abc


class SlackAPI(abc.SlackAPI):

    def _request(self, method, url, headers, body):

        response = requests.request(method, url, headers=headers, data=body)
        return response.status_code, response.headers, response.content

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def postiter(self, *args, **kwargs):
        yield from super().postiter(*args, **kwargs)
