import json
import time
import asyncio
import datetime

import asks
import trio
import curio
import pytest
import aiohttp
import requests
import asynctest
import slack
from slack import methods, exceptions
from slack.io.trio import SlackAPI as SlackAPITrio
from slack.io.curio import SlackAPI as SlackAPICurio
from slack.io.aiohttp import SlackAPI as SlackAPIAiohttp
from slack.io.requests import SlackAPI as SlackAPIRequest


@pytest.mark.asyncio
class TestABC:
    async def test_query(self, slack_client, token):
        rep = await slack_client.query(methods.AUTH_TEST)
        slack_client._request.assert_called_once()
        assert slack_client._request.call_args[0][0] == "POST"
        assert (
            slack_client._request.call_args[0][1] == "https://slack.com/api/auth.test"
        )
        assert slack_client._request.call_args[0][2] == {
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        }
        assert slack_client._request.call_args[0][3] == "{}"

        assert rep == {"ok": True}

    async def test_query_url(self, slack_client):
        await slack_client.query("auth.test")
        assert (
            slack_client._request.call_args[0][1] == "https://slack.com/api/auth.test"
        )

    async def test_query_long_url(self, slack_client):
        await slack_client.query("https://slack.com/api/auth.test")
        assert (
            slack_client._request.call_args[0][1] == "https://slack.com/api/auth.test"
        )

    async def test_query_webhook_url(self, slack_client):
        await slack_client.query("https://hooks.slack.com/abcdef")
        assert slack_client._request.call_args[0][1] == "https://hooks.slack.com/abcdef"

    async def test_query_data(self, slack_client, token):
        data = {"hello": "world"}

        called_with = json.dumps(data.copy())

        await slack_client.query(methods.AUTH_TEST, data)
        assert slack_client._request.call_args[0][3] == called_with

    async def test_query_data_webhook(self, slack_client, token):
        data = {"hello": "world"}

        called_with = data.copy()

        await slack_client.query("https://hooks.slack.com/abcdef", data)
        assert slack_client._request.call_args[0][3] == json.dumps(called_with)

    async def test_query_headers(self, slack_client, token):
        custom_headers = {
            "hello": "world",
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        }
        called_headers = custom_headers.copy()

        await slack_client.query(
            "https://hooks.slack.com/abcdef", headers=custom_headers
        )
        assert slack_client._request.call_args[0][2] == called_headers

    @pytest.mark.parametrize(
        "slack_client", ({"body": ["channels_iter", "channels"]},), indirect=True
    )
    async def test_iter(self, slack_client, token, itercursor):
        channels = 0
        async for _ in slack_client.iter(methods.CHANNELS_LIST):  # noQa: F841
            channels += 1

        assert channels == 4
        assert slack_client._request.call_count == 2
        slack_client._request.assert_called_with(
            "POST",
            "https://slack.com/api/channels.list",
            {},
            {"limit": 200, "token": token, "cursor": itercursor},
        )

    @pytest.mark.parametrize(
        "slack_client", ({"body": ["channels_iter", "channels"]},), indirect=True
    )
    async def test_iter_itermode_iterkey(self, slack_client, token, itercursor):
        channels = 0
        async for _ in slack_client.iter(
            "channels.list", itermode="cursor", iterkey="channels"
        ):  # noQa: F841
            channels += 1

        assert channels == 4
        assert slack_client._request.call_count == 2
        slack_client._request.assert_called_with(
            "POST",
            "https://slack.com/api/channels.list",
            {},
            {"limit": 200, "token": token, "cursor": itercursor},
        )

    async def test_iter_not_supported(self, slack_client):
        with pytest.raises(ValueError):
            async for _ in slack_client.iter(methods.AUTH_TEST):  # noQa: F841
                pass

        with pytest.raises(ValueError):
            async for _ in slack_client.iter("channels.list"):  # noQa: F841
                pass

        with pytest.raises(ValueError):
            async for _ in slack_client.iter(
                "https://slack.com/api/channels.list"
            ):  # noQa: F841
                pass

    @pytest.mark.parametrize(
        "slack_client", ({"body": ["channels_iter", "channels"]},), indirect=True
    )
    async def test_iter_wait(self, slack_client):
        slack_client.sleep = asynctest.CoroutineMock()

        channels = 0
        async for _ in slack_client.iter(
            methods.CHANNELS_LIST, minimum_time=2
        ):  # noQa: F841
            channels += 1

        assert channels == 4
        assert slack_client._request.call_count == 2
        assert slack_client.sleep.call_count == 1
        assert 2 > slack_client.sleep.call_args[0][0] > 1.9

    @pytest.mark.parametrize(
        "slack_client", ({"body": ["channels_iter", "channels"]},), indirect=True
    )
    async def test_iter_no_wait(self, slack_client):
        slack_client.sleep = asynctest.CoroutineMock()

        channels = 0
        async for _ in slack_client.iter(
            methods.CHANNELS_LIST, minimum_time=1
        ):  # noQa: F841
            channels += 1
            await asyncio.sleep(0.5)

        assert channels == 4
        assert slack_client._request.call_count == 2
        assert slack_client.sleep.call_count == 0

    @pytest.mark.parametrize(
        "slack_client", ({"body": ["auth_test", "users_info"]},), indirect=True
    )
    async def test_find_bot_id(self, slack_client):
        bot_id = await slack_client._find_bot_id()
        assert bot_id == "B0AAA0A00"

    @pytest.mark.parametrize("slack_client", ({"body": "rtm_connect"},), indirect=True)
    async def test_find_rtm_url(self, slack_client):
        url = await slack_client._find_rtm_url()
        assert url == "wss://testteam.slack.com/012345678910"

    async def test_incoming_rtm(self, slack_client, rtm_iterator):
        slack_client._rtm = rtm_iterator

        events = []
        async for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            assert isinstance(event, slack.events.Event)
            events.append(event)
        assert len(events) > 0

    @pytest.mark.parametrize("rtm_iterator", (("goodbye",),), indirect=True)
    async def test_incoming_rtm_reconnect(self, slack_client, rtm_iterator):
        slack_client._rtm = rtm_iterator

        events = []
        async for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize("rtm_iterator", (("message_bot",),), indirect=True)
    async def test_incoming_rtm_discard_bot_id(self, slack_client, rtm_iterator):
        slack_client._rtm = rtm_iterator

        events = []
        async for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize("rtm_iterator", (("reconnect_url",),), indirect=True)
    async def test_incoming_rtm_skip(self, slack_client, rtm_iterator):
        slack_client._rtm = rtm_iterator

        events = []
        async for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            events.append(event)

        assert len(events) == 0


class TestNoAsync:
    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    def test_query(self, slack_client, token):
        rep = slack_client.query(methods.AUTH_TEST)
        slack_client._request.assert_called_once()
        assert slack_client._request.call_args[0][0] == "POST"
        assert (
            slack_client._request.call_args[0][1] == "https://slack.com/api/auth.test"
        )
        assert slack_client._request.call_args[0][2] == {
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        }
        assert slack_client._request.call_args[0][3] == "{}"

        assert rep == {"ok": True}

    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    def test_query_data(self, slack_client):
        data = {"hello": "world"}

        called_with = json.dumps(data.copy())

        slack_client.query(methods.AUTH_TEST, data)
        assert slack_client._request.call_args[0][3] == called_with

    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    def test_query_headers(self, slack_client, token):
        custom_headers = {
            "hello": "world",
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        }
        called_headers = custom_headers.copy()

        slack_client.query("https://hooks.slack.com/abcdef", headers=custom_headers)
        assert slack_client._request.call_args[0][2] == called_headers

    @pytest.mark.parametrize(
        "slack_client",
        ({"client": SlackAPIRequest, "body": ["channels_iter", "channels"]},),
        indirect=True,
    )
    def test_iter(self, slack_client, token, itercursor):
        channels = 0
        for _ in slack_client.iter(methods.CHANNELS_LIST):  # noQa: F841
            channels += 1

        assert channels == 4
        assert slack_client._request.call_count == 2
        slack_client._request.assert_called_with(
            "POST",
            "https://slack.com/api/channels.list",
            {},
            {"limit": 200, "token": token, "cursor": itercursor},
        )

    @pytest.mark.parametrize(
        "slack_client",
        ({"client": SlackAPIRequest, "body": ["channels_iter", "channels"]},),
        indirect=True,
    )
    def test_iter_wait(self, slack_client):
        slack_client.sleep = asynctest.CoroutineMock()

        channels = 0
        for _ in slack_client.iter(methods.CHANNELS_LIST, minimum_time=2):  # noQa: F841
            channels += 1

        assert channels == 4
        assert slack_client._request.call_count == 2
        assert slack_client.sleep.call_count == 1
        assert 2 > slack_client.sleep.call_args[0][0] > 1.9

    @pytest.mark.parametrize(
        "slack_client",
        ({"client": SlackAPIRequest, "body": ["channels_iter", "channels"]},),
        indirect=True,
    )
    def test_iter_no_wait(self, slack_client):
        slack_client.sleep = asynctest.CoroutineMock()

        channels = 0
        for _ in slack_client.iter(methods.CHANNELS_LIST, minimum_time=1):  # noQa: F841
            channels += 1
            time.sleep(0.5)

        assert channels == 4
        assert slack_client._request.call_count == 2
        assert slack_client.sleep.call_count == 0

    @pytest.mark.parametrize(
        "slack_client",
        ({"client": SlackAPIRequest, "body": ["auth_test", "users_info"]},),
        indirect=True,
    )
    def test_find_bot_id(self, slack_client):
        bot_id = slack_client._find_bot_id()
        assert bot_id == "B0AAA0A00"

    @pytest.mark.parametrize(
        "slack_client",
        ({"client": SlackAPIRequest, "body": "rtm_connect"},),
        indirect=True,
    )
    def test_find_rtm_url(self, slack_client):
        url = slack_client._find_rtm_url()
        assert url == "wss://testteam.slack.com/012345678910"

    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    def test_incoming_rtm(self, slack_client, rtm_iterator_non_async):
        slack_client._rtm = rtm_iterator_non_async

        events = []
        for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            assert isinstance(event, slack.events.Event)
            events.append(event)
        assert len(events) > 0

    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    @pytest.mark.parametrize("rtm_iterator_non_async", (("goodbye",),), indirect=True)
    def test_incoming_rtm_reconnect(self, slack_client, rtm_iterator_non_async):
        slack_client._rtm = rtm_iterator_non_async

        events = []
        for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    @pytest.mark.parametrize(
        "rtm_iterator_non_async", (("message_bot",),), indirect=True
    )
    def test_incoming_rtm_discard_bot_id(self, slack_client, rtm_iterator_non_async):
        slack_client._rtm = rtm_iterator_non_async

        events = []
        for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.parametrize(
        "slack_client", ({"client": SlackAPIRequest},), indirect=True
    )
    @pytest.mark.parametrize(
        "rtm_iterator_non_async", (("reconnect_url",),), indirect=True
    )
    def test_incoming_rtm_skip(self, slack_client, rtm_iterator_non_async):
        slack_client._rtm = rtm_iterator_non_async

        events = []
        for event in slack_client._incoming_from_rtm(
            "wss://testteam.slack.com/012345678910", "B0AAA0A00"
        ):
            events.append(event)

        assert len(events) == 0


class TestRequest:
    def test_sleep(self, token):
        delay = 1
        start = datetime.datetime.now()
        with requests.Session() as session:
            slack_client = SlackAPIRequest(session=session, token=token)
            slack_client.sleep(delay)
        stop = datetime.datetime.now()
        assert (
            datetime.timedelta(seconds=delay + 1)
            > (stop - start)
            > datetime.timedelta(seconds=delay)
        )

    def test__request(self, token):
        with requests.Session() as session:
            slack_client = SlackAPIRequest(session=session, token=token)
            response = slack_client._request(
                "POST", "https://slack.com/api//api.test", {}, {"token": token}
            )

        assert response[0] == 200
        assert response[1] == b'{"ok":false,"error":"invalid_auth"}'


class TestAiohttp:
    @pytest.mark.asyncio
    async def test_sleep(self, token):
        delay = 1
        start = datetime.datetime.now()
        async with aiohttp.ClientSession() as session:
            slack_client = SlackAPIAiohttp(session=session, token=token)
            await slack_client.sleep(delay)
        stop = datetime.datetime.now()
        assert (
            datetime.timedelta(seconds=delay + 1)
            > (stop - start)
            > datetime.timedelta(seconds=delay)
        )

    @pytest.mark.asyncio
    async def test__request(self, token):
        async with aiohttp.ClientSession() as session:
            slack_client = SlackAPIAiohttp(session=session, token=token)
            response = await slack_client._request(
                "POST", "https://slack.com/api//api.test", {}, {"token": token}
            )

        assert response[0] == 200
        assert response[1] == b'{"ok":false,"error":"invalid_auth"}'


class TestTrio:
    def test_sleep(self, token):
        async def test_function():
            delay = 1
            start = datetime.datetime.now()
            session = asks.Session()
            slack_client = SlackAPITrio(session=session, token=token)
            await slack_client.sleep(delay)
            stop = datetime.datetime.now()
            return (
                datetime.timedelta(seconds=delay + 1)
                > (stop - start)
                > datetime.timedelta(seconds=delay)
            )

        assert trio.run(test_function)

    def test__request(self, token):
        async def test_function():
            session = asks.Session()
            slack_client = SlackAPITrio(session=session, token=token)
            response = await slack_client._request(
                "POST", "https://slack.com/api//api.test", {}, {"token": token}
            )
            return response[0], response[1]

        assert trio.run(test_function) == (200, b'{"ok":false,"error":"invalid_auth"}')


class TestCurio:
    def test_sleep(self, token):
        async def test_function():
            delay = 1
            start = datetime.datetime.now()
            session = asks.Session()
            slack_client = SlackAPICurio(session=session, token=token)
            await slack_client.sleep(delay)
            stop = datetime.datetime.now()
            return (
                datetime.timedelta(seconds=delay + 1)
                > (stop - start)
                > datetime.timedelta(seconds=delay)
            )

        assert curio.run(test_function)

    def test__request(self, token):
        async def test_function():
            session = asks.Session()
            slack_client = SlackAPICurio(session=session, token=token)
            response = await slack_client._request(
                "POST", "https://slack.com/api//api.test", {}, {"token": token}
            )
            return response[0], response[1]

        assert curio.run(test_function) == (200, b'{"ok":false,"error":"invalid_auth"}')
