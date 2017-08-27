import json
import pytest
import asynctest

from slack import methods, exceptions


def return_value(method):
    if method == methods.AUTH_TEST:
        return 200, b'{"ok": true}', {'content-type': 'application/json; charset=utf-8'}


@pytest.mark.asyncio
class TestABC:

    async def test_query(self, client, headers, ok_body):
        client._request = asynctest.CoroutineMock(return_value=(200, ok_body, headers))
        rep = await client.query(methods.AUTH_TEST)

        client._request.assert_called_once()
        assert client._request.call_args[0][0] == 'POST'
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'
        assert client._request.call_args[0][2] == {}
        assert client._request.call_args[0][3] == {'token': 'abcdefg'}

        assert rep == {'ok': True}

    async def test_query_url(self, client, headers, ok_body):
        client._request = asynctest.CoroutineMock(return_value=(200, ok_body, headers))
        await client.query('auth.test')
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'

    async def test_query_long_url(self, client, headers, ok_body):
        client._request = asynctest.CoroutineMock(return_value=(200, ok_body, headers))
        await client.query('https://slack.com/api/auth.test')
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'

    async def test_query_webhook_url(self, client, headers, ok_body):
        client._request = asynctest.CoroutineMock(return_value=(200, ok_body, headers))
        await client.query('https://hooks.slack.com/abcdef')
        assert client._request.call_args[0][1] == 'https://hooks.slack.com/abcdef'

    async def test_query_data(self, client, headers, ok_body, token):
        data = {'hello': 'world'}

        rep = data.copy()
        rep['token'] = token

        client._request = asynctest.CoroutineMock(return_value=(200, ok_body, headers))
        await client.query(methods.AUTH_TEST, data)
        assert client._request.call_args[0][3] == rep

    async def test_query_data_webhook(self, client, token):
        data = {'hello': 'world'}

        rep = data.copy()
        rep['token'] = token

        client._request = asynctest.CoroutineMock(return_value=return_value(methods.AUTH_TEST))
        await client.query('https://hooks.slack.com/abcdef', data)
        assert client._request.call_args[0][3] == json.dumps(rep)

    async def test_query_headers(self, client, headers, ok_body):
        custom_headers = {'hello': 'world'}
        called_headers = custom_headers.copy()

        client._request = asynctest.CoroutineMock(return_value=(200, ok_body, headers))
        await client.query('https://hooks.slack.com/abcdef', headers=custom_headers)
        assert client._request.call_args[0][2] == called_headers

    async def test_retry_rate_limited(self, client, headers_rate_limit, nok_body, ok_body, headers):
        client._request = asynctest.CoroutineMock(side_effect=(
            (429, nok_body, headers_rate_limit),
            (200, ok_body, headers)
        ))
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        await client.query(methods.AUTH_TEST)
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(2)

    @pytest.mark.parametrize('client', ('raise',), indirect=True)
    async def test_raise_rate_limited(self, client, headers_rate_limit, nok_body):
        client._request = asynctest.CoroutineMock(return_value=(429, nok_body, headers_rate_limit))
        with pytest.raises(exceptions.RateLimited):
            await client.query(methods.AUTH_TEST)

    async def test_iter(self, client, channels_iter, channels, headers):
        client._request = asynctest.CoroutineMock(side_effect=(
            (200, channels_iter, headers),
            (200, channels, headers)
        ))
        channels = 0
        async for _ in client.iter(methods.CHANNELS_LIST):
            channels += 1

        assert channels == 4
        assert client._request.call_count == 2
        client._request.assert_called_with(
            'POST', 'https://slack.com/api/channels.list', {}, {'limit': 200, 'token': 'abcdefg', 'cursor': 'wxyz'}
        )

    async def test_iter_itermode_iterkey(self, client, channels_iter, channels, headers):
        client._request = asynctest.CoroutineMock(side_effect=(
            (200, channels_iter, headers),
            (200, channels, headers)
        ))
        channels = 0
        async for _ in client.iter('channels.list', itermode='cursor', iterkey='channels'):
            channels += 1

        assert channels == 4
        assert client._request.call_count == 2
        client._request.assert_called_with(
            'POST', 'https://slack.com/api/channels.list', {}, {'limit': 200, 'token': 'abcdefg', 'cursor': 'wxyz'}
        )

    async def test_iter_not_supported(self, client):
        with pytest.raises(ValueError):
            async for _ in client.iter(methods.AUTH_TEST):
                pass

        with pytest.raises(ValueError):
            async for _ in client.iter('channels.list'):
                pass

        with pytest.raises(ValueError):
            async for _ in client.iter('https://slack.com/api/channels.list'):
                pass
