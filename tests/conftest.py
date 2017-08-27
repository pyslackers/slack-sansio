import time
import pytest

from slack.io.abc import SlackAPI


TOKEN = 'abcdefg'


@pytest.fixture()
def headers():
    return {'content-type': 'application/json; charset=utf-8'}


@pytest.fixture()
def headers_rate_limit(headers):
    headers['Retry-After'] = 2
    return headers


@pytest.fixture()
def token():
    return TOKEN


@pytest.fixture()
def channels():
    with open('tests/data/channels.json', 'rb') as f:
        return f.read()


@pytest.fixture()
def channels_iter():
    with open('tests/data/channels_iter.json', 'rb') as f:
        return f.read()


@pytest.fixture()
def ok_body():
    return b'{"ok": true}'


@pytest.fixture()
def nok_body():
    return b'{"ok": false}'


class FakeIO(SlackAPI):
    async def _request(self, method, url, headers, body):
        pass

    async def sleep(self, seconds):
        time.sleep(seconds)

    async def _rtm(self, url):
        pass


@pytest.fixture()
def client(request):

    if hasattr(request, 'param'):
        if 'raise' in request.param:
            return FakeIO(token=TOKEN, retry_when_rate_limit=False)

    return FakeIO(token=TOKEN)
