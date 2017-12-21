import json
import pytest
import asynctest

from slack import methods, exceptions


@pytest.mark.asyncio
class TestABC:

    async def test_query(self, client):
        rep = await client.query(methods.AUTH_TEST)
        client._request.assert_called_once()
        assert client._request.call_args[0][0] == 'POST'
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'
        assert client._request.call_args[0][2] == {}
        assert client._request.call_args[0][3] == {'token': 'abcdefg'}

        assert rep == {'ok': True}

    async def test_query_url(self, client):
        await client.query('auth.test')
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'

    async def test_query_long_url(self, client):
        await client.query('https://slack.com/api/auth.test')
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'

    async def test_query_webhook_url(self, client):
        await client.query('https://hooks.slack.com/abcdef')
        assert client._request.call_args[0][1] == 'https://hooks.slack.com/abcdef'

    async def test_query_data(self, client, token):
        data = {'hello': 'world'}

        called_with = data.copy()
        called_with['token'] = token

        await client.query(methods.AUTH_TEST, data)
        assert client._request.call_args[0][3] == called_with

    async def test_query_data_webhook(self, client, token):
        data = {'hello': 'world'}

        called_with = data.copy()
        called_with['token'] = token

        await client.query('https://hooks.slack.com/abcdef', data)
        assert client._request.call_args[0][3] == json.dumps(called_with)

    async def test_query_headers(self, client):
        custom_headers = {'hello': 'world'}
        called_headers = custom_headers.copy()

        await client.query('https://hooks.slack.com/abcdef', headers=custom_headers)
        assert client._request.call_args[0][2] == called_headers

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]}, ), indirect=True)
    async def test_retry_rate_limited(self, client):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        await client.query(methods.AUTH_TEST)
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request':
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 2}}
                                         }, ), indirect=True)
    async def test_raise_rate_limited(self, client):
        with pytest.raises(exceptions.RateLimited):
            await client.query(methods.AUTH_TEST)

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request': [
                                             {'body': 'channels_iter'},
                                             {'body': 'channels'}
                                         ]}, ), indirect=True)
    async def test_iter(self, client, token, itercursor):
        channels = 0
        async for _ in client.iter(methods.CHANNELS_LIST):  # noQa: F841
            channels += 1

        assert channels == 4
        assert client._request.call_count == 2
        client._request.assert_called_with(
            'POST', 'https://slack.com/api/channels.list', {}, {'limit': 200, 'token': token, 'cursor': itercursor}
        )

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request': [
                                             {'body': 'channels_iter'},
                                             {'body': 'channels'}
                                         ]}, ), indirect=True)
    async def test_iter_itermode_iterkey(self, client, token, itercursor):
        channels = 0
        async for _ in client.iter('channels.list', itermode='cursor', iterkey='channels'):  # noQa: F841
            channels += 1

        assert channels == 4
        assert client._request.call_count == 2
        client._request.assert_called_with(
            'POST', 'https://slack.com/api/channels.list', {}, {'limit': 200, 'token': token, 'cursor': itercursor}
        )

    async def test_iter_not_supported(self, client):
        with pytest.raises(ValueError):
            async for _ in client.iter(methods.AUTH_TEST):  # noQa: F841
                pass

        with pytest.raises(ValueError):
            async for _ in client.iter('channels.list'):  # noQa: F841
                pass

        with pytest.raises(ValueError):
            async for _ in client.iter('https://slack.com/api/channels.list'):  # noQa: F841
                pass
