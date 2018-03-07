import json
import asks
import trio
import time
import slack
import curio
import pytest
import asyncio
import aiohttp
import requests
import datetime
import asynctest

from slack import methods, exceptions

from slack.io.trio import SlackAPI as SlackAPITrio
from slack.io.curio import SlackAPI as SlackAPICurio
from slack.io.aiohttp import SlackAPI as SlackAPIAiohttp
from slack.io.requests import SlackAPI as SlackAPIRequest


@pytest.mark.asyncio
class TestABC:

    async def test_query(self, client, token):
        rep = await client.query(methods.AUTH_TEST)
        client._request.assert_called_once()
        assert client._request.call_args[0][0] == 'POST'
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'
        assert client._request.call_args[0][2] == {
            'Content-type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {token}'
        }
        assert client._request.call_args[0][3] == '{}'

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

        called_with = json.dumps(data.copy())

        await client.query(methods.AUTH_TEST, data)
        assert client._request.call_args[0][3] == called_with

    async def test_query_data_webhook(self, client, token):
        data = {'hello': 'world'}

        called_with = data.copy()

        await client.query('https://hooks.slack.com/abcdef', data)
        assert client._request.call_args[0][3] == json.dumps(called_with)

    async def test_query_headers(self, client, token):
        custom_headers = {'hello': 'world',
                          'Content-type': 'application/json; charset=utf-8',
                          'Authorization': f'Bearer {token}'}
        called_headers = custom_headers.copy()

        await client.query('https://hooks.slack.com/abcdef', headers=custom_headers)
        assert client._request.call_args[0][2] == called_headers

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]}, ), indirect=True)
    async def test_retry_rate_limited(self, client, token):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        rep = await client.query(methods.AUTH_TEST)
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)
        assert client._request.call_args_list[0] == client._request.call_args_list[1]
        args, kwargs = client._request.call_args_list[0]
        assert args == ('POST', 'https://slack.com/api/auth.test',
                        {'Content-type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {token}'},
                        '{}')
        assert kwargs == {}
        assert rep == {'ok': True}

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]}, ), indirect=True)
    async def test_retry_rate_limited_with_body(self, client, token):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        await client.query(methods.AUTH_TEST, data={'foo': 'bar'})
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)
        assert client._request.call_args_list[0] == client._request.call_args_list[1]
        args, kwargs = client._request.call_args_list[0]
        assert args == ('POST', 'https://slack.com/api/auth.test',
                        {'Content-type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {token}'},
                        '{"foo": "bar"}')
        assert kwargs == {}

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]}, ), indirect=True)
    async def test_retry_rate_limited_with_headers(self, client, token):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        await client.query(methods.AUTH_TEST, headers={'foo': 'bar'})
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)
        assert client._request.call_args_list[0] == client._request.call_args_list[1]
        args, kwargs = client._request.call_args_list[0]
        assert args == ('POST', 'https://slack.com/api/auth.test',
                        {'foo': 'bar',
                         'Content-type': 'application/json; charset=utf-8',
                         'Authorization': f'Bearer {token}'},
                        '{}')
        assert kwargs == {}

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

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request': [
                                             {'body': 'channels_iter'},
                                             {'body': 'channels'}
                                         ]}, ), indirect=True)
    async def test_iter_wait(self, client):
        client.sleep = asynctest.CoroutineMock()

        channels = 0
        async for _ in client.iter(methods.CHANNELS_LIST, minimum_time=2):  # noQa: F841
            channels += 1

        assert channels == 4
        assert client._request.call_count == 2
        assert client.sleep.call_count == 1
        assert 2 > client.sleep.call_args[0][0] > 1.9

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request': [
                                             {'body': 'channels_iter'},
                                             {'body': 'channels'}
                                         ]}, ), indirect=True)
    async def test_iter_no_wait(self, client):
        client.sleep = asynctest.CoroutineMock()

        channels = 0
        async for _ in client.iter(methods.CHANNELS_LIST, minimum_time=1):  # noQa: F841
            channels += 1
            await asyncio.sleep(0.5)

        assert channels == 4
        assert client._request.call_count == 2
        assert client.sleep.call_count == 0

    @pytest.mark.parametrize('client', ({'_request': [{'body': 'auth_test'}, {'body': 'users_info'}]}, ), indirect=True)
    async def test_find_bot_id(self, client):
        bot_id = await client._find_bot_id()
        assert bot_id == 'B0AAA0A00'

    @pytest.mark.parametrize('client', ({'_request': {'body': 'rtm_connect'}}, ), indirect=True)
    async def test_find_rtm_url(self, client):
        url = await client._find_rtm_url()
        assert url == 'wss:\/\/testteam.slack.com/012345678910'

    async def test_incoming_rtm(self, client, rtm_iterator):
        client._rtm = rtm_iterator

        events = []
        async for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            assert isinstance(event, slack.events.Event)
            events.append(event)
        assert len(events) > 0

    @pytest.mark.parametrize('rtm_iterator', (('goodbye', ), ), indirect=True)
    async def test_incoming_rtm_reconnect(self, client, rtm_iterator):
        client._rtm = rtm_iterator

        events = []
        async for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize('rtm_iterator', (('message_bot', ), ), indirect=True)
    async def test_incoming_rtm_discard_bot_id(self, client, rtm_iterator):
        client._rtm = rtm_iterator

        events = []
        async for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize('rtm_iterator', (('reconnect_url', ), ), indirect=True)
    async def test_incoming_rtm_skip(self, client, rtm_iterator):
        client._rtm = rtm_iterator

        events = []
        async for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            events.append(event)

        assert len(events) == 0


@pytest.mark.parametrize('io_client', (SlackAPIRequest, ), indirect=True)
class TestNoAsync:
    def test_query(self, client, token):
        rep = client.query(methods.AUTH_TEST)
        client._request.assert_called_once()
        assert client._request.call_args[0][0] == 'POST'
        assert client._request.call_args[0][1] == 'https://slack.com/api/auth.test'
        assert client._request.call_args[0][2] == {
            'Content-type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {token}'
        }
        assert client._request.call_args[0][3] == '{}'

        assert rep == {'ok': True}

    def test_query_data(self, client):
        data = {'hello': 'world'}

        called_with = json.dumps(data.copy())

        client.query(methods.AUTH_TEST, data)
        assert client._request.call_args[0][3] == called_with

    def test_query_headers(self, client, token):
        custom_headers = {'hello': 'world',
                          'Content-type': 'application/json; charset=utf-8',
                          'Authorization': f'Bearer {token}'}
        called_headers = custom_headers.copy()

        client.query('https://hooks.slack.com/abcdef', headers=custom_headers)
        assert client._request.call_args[0][2] == called_headers

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]},), indirect=True)
    def test_retry_rate_limited(self, client, token):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        rep = client.query(methods.AUTH_TEST)
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)
        assert client._request.call_args_list[0] == client._request.call_args_list[1]
        args, kwargs = client._request.call_args_list[0]
        assert args == ('POST', 'https://slack.com/api/auth.test',
                        {'Content-type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {token}'},
                        '{}')
        assert kwargs == {}
        assert rep == {'ok': True}

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]},), indirect=True)
    def test_retry_rate_limited_with_body(self, client, token):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        client.query(methods.AUTH_TEST, data={'foo': 'bar'})
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)
        assert client._request.call_args_list[0] == client._request.call_args_list[1]
        args, kwargs = client._request.call_args_list[0]
        assert args == ('POST', 'https://slack.com/api/auth.test',
                        {'Content-type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {token}'},
                        '{"foo": "bar"}')
        assert kwargs == {}

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': True,
                                         '_request': [
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 1}},
                                             {},
                                         ]},), indirect=True)
    def test_retry_rate_limited_with_headers(self, client, token):
        client.sleep = asynctest.CoroutineMock(side_effect=client.sleep)
        client.query(methods.AUTH_TEST, headers={'foo': 'bar'})
        assert client._request.call_count == 2
        client.sleep.assert_called_once_with(1)
        assert client._request.call_args_list[0] == client._request.call_args_list[1]
        args, kwargs = client._request.call_args_list[0]
        assert args == ('POST', 'https://slack.com/api/auth.test',
                        {'foo': 'bar',
                         'Content-type': 'application/json; charset=utf-8',
                         'Authorization': f'Bearer {token}'},
                        '{}')
        assert kwargs == {}

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request':
                                             {'status': 429, 'body': {"ok": False}, 'headers': {'Retry-After': 2}}
                                         },), indirect=True)
    def test_raise_rate_limited(self, client):
        with pytest.raises(exceptions.RateLimited):
            client.query(methods.AUTH_TEST)

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request': [
                                             {'body': 'channels_iter'},
                                             {'body': 'channels'}
                                         ]}, ), indirect=True)
    def test_iter(self, client, token, itercursor):
        channels = 0
        for _ in client.iter(methods.CHANNELS_LIST):  # noQa: F841
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
    def test_iter_wait(self, client):
        client.sleep = asynctest.CoroutineMock()

        channels = 0
        for _ in client.iter(methods.CHANNELS_LIST, minimum_time=2):  # noQa: F841
            channels += 1

        assert channels == 4
        assert client._request.call_count == 2
        assert client.sleep.call_count == 1
        assert 2 > client.sleep.call_args[0][0] > 1.9

    @pytest.mark.parametrize('client', ({'retry_when_rate_limit': False,
                                         '_request': [
                                             {'body': 'channels_iter'},
                                             {'body': 'channels'}
                                         ]}, ), indirect=True)
    def test_iter_no_wait(self, client):
        client.sleep = asynctest.CoroutineMock()

        channels = 0
        for _ in client.iter(methods.CHANNELS_LIST, minimum_time=1):  # noQa: F841
            channels += 1
            time.sleep(0.5)

        assert channels == 4
        assert client._request.call_count == 2
        assert client.sleep.call_count == 0

    @pytest.mark.parametrize('client', ({'_request': [{'body': 'auth_test'}, {'body': 'users_info'}]}, ), indirect=True)
    def test_find_bot_id(self, client):
        bot_id = client._find_bot_id()
        assert bot_id == 'B0AAA0A00'

    @pytest.mark.parametrize('client', ({'_request': {'body': 'rtm_connect'}}, ), indirect=True)
    def test_find_rtm_url(self, client):
        url = client._find_rtm_url()
        assert url == 'wss:\/\/testteam.slack.com/012345678910'

    def test_incoming_rtm(self, client, rtm_iterator_non_async):
        client._rtm = rtm_iterator_non_async

        events = []
        for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            assert isinstance(event, slack.events.Event)
            events.append(event)
        assert len(events) > 0

    @pytest.mark.parametrize('rtm_iterator_non_async', (('goodbye', ), ), indirect=True)
    def test_incoming_rtm_reconnect(self, client, rtm_iterator_non_async):
        client._rtm = rtm_iterator_non_async

        events = []
        for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize('rtm_iterator_non_async', (('message_bot', ), ), indirect=True)
    def test_incoming_rtm_discard_bot_id(self, client, rtm_iterator_non_async):
        client._rtm = rtm_iterator_non_async

        events = []
        for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize('rtm_iterator_non_async', (('reconnect_url', ), ), indirect=True)
    def test_incoming_rtm_skip(self, client, rtm_iterator_non_async):
        client._rtm = rtm_iterator_non_async

        events = []
        for event in client._incoming_from_rtm('wss:\/\/testteam.slack.com/012345678910', 'B0AAA0A00'):
            events.append(event)

        assert len(events) == 0


class TestRequest:
    def test_sleep(self, token):
        delay = 1
        start = datetime.datetime.now()
        with requests.Session() as session:
            client = SlackAPIRequest(session=session, token=token)
            client.sleep(delay)
        stop = datetime.datetime.now()
        assert datetime.timedelta(seconds=delay + 1) > (stop - start) > datetime.timedelta(seconds=delay)

    def test__request(self, token):
        with requests.Session() as session:
            client = SlackAPIRequest(session=session, token=token)
            response = client._request('POST', 'https://slack.com/api//api.test', {}, {'token': token})

        assert response[0] == 200
        assert response[1] == b'{"ok":false,"error":"invalid_auth"}'


class TestAiohttp:
    @pytest.mark.asyncio
    async def test_sleep(self, token):
        delay = 1
        start = datetime.datetime.now()
        async with aiohttp.ClientSession() as session:
            client = SlackAPIAiohttp(session=session, token=token)
            await client.sleep(delay)
        stop = datetime.datetime.now()
        assert datetime.timedelta(seconds=delay + 1) > (stop - start) > datetime.timedelta(seconds=delay)

    @pytest.mark.asyncio
    async def test__request(self, token):
        async with aiohttp.ClientSession() as session:
            client = SlackAPIAiohttp(session=session, token=token)
            response = await client._request('POST', 'https://slack.com/api//api.test', {}, {'token': token})

        assert response[0] == 200
        assert response[1] == b'{"ok":false,"error":"invalid_auth"}'


class TestTrio:
    def test_sleep(self, token):
        asks.init('trio')

        async def test_function():
            delay = 1
            start = datetime.datetime.now()
            session = asks.Session()
            client = SlackAPITrio(session=session, token=token)
            await client.sleep(delay)
            stop = datetime.datetime.now()
            return datetime.timedelta(seconds=delay + 1) > (stop - start) > datetime.timedelta(seconds=delay)

        assert trio.run(test_function)

    def test__request(self, token):
        asks.init('trio')

        async def test_function():
            session = asks.Session()
            client = SlackAPITrio(session=session, token=token)
            response = await client._request('POST', 'https://slack.com/api//api.test', {}, {'token': token})
            return response[0], response[1]
        assert trio.run(test_function) == (200, b'{"ok":false,"error":"invalid_auth"}')


class TestCurio:
    def test_sleep(self, token):
        asks.init('curio')

        async def test_function():
            delay = 1
            start = datetime.datetime.now()
            session = asks.Session()
            client = SlackAPICurio(session=session, token=token)
            await client.sleep(delay)
            stop = datetime.datetime.now()
            return datetime.timedelta(seconds=delay + 1) > (stop - start) > datetime.timedelta(seconds=delay)

        assert curio.run(test_function)

    def test__request(self, token):
        asks.init('curio')

        async def test_function():
            session = asks.Session()
            client = SlackAPICurio(session=session, token=token)
            response = await client._request('POST', 'https://slack.com/api//api.test', {}, {'token': token})
            return response[0], response[1]
        assert curio.run(test_function) == (200, b'{"ok":false,"error":"invalid_auth"}')
