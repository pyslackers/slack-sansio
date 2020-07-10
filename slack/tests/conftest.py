import copy
import json
import time
from unittest.mock import Mock

import pytest
import asynctest
from slack.events import EventRouter, MessageRouter
from slack.io.abc import SlackAPI
from slack.actions import Router as ActionRouter
from slack.commands import Router as CommandRouter

from . import data

try:
    from slack.io.requests import SlackAPI as SlackAPIRequest
except ImportError:
    SlackAPIRequest = int  # type: ignore

TOKEN = "abcdefg"


class FakeIO(SlackAPI):
    async def _request(self, method, url, headers, body):
        pass

    async def sleep(self, seconds):
        time.sleep(seconds)

    async def _rtm(self, url):
        pass


@pytest.fixture(params=(data.RTMEvents.__members__,))
def rtm_iterator(request):
    async def events(url):
        for key in request.param:
            yield data.RTMEvents[key].value

    return events


@pytest.fixture(params=(data.RTMEvents.__members__,))
def rtm_iterator_non_async(request):
    def events(url):
        for key in request.param:
            yield data.RTMEvents[key].value

    return events


def _slack_client_default_parameters(parameters):
    if "status" not in parameters:
        parameters["status"] = 200

    if "body" not in parameters:
        parameters["body"] = {"ok": True}

    if "headers" not in parameters:
        parameters["headers"] = {"content-type": "application/json; charset=utf-8"}

    client_param = parameters.get("client_parameters", {})
    if "token" not in client_param:
        client_param["token"] = TOKEN

    parameters["client_parameters"] = client_param
    return parameters


def _slack_client(parameters):
    if "client" in parameters:
        client = parameters["client"]
    else:
        client = FakeIO

    slackclient = client(**parameters["client_parameters"])

    return slackclient


def _slack_client_single_mock_request(slackclient, parameters):
    return_value = (
        parameters["status"],
        json.dumps(_fill_body(parameters["body"])).encode(),
        parameters["headers"],
    )

    if isinstance(slackclient, SlackAPIRequest):
        slackclient._request = Mock(return_value=return_value)
    else:
        slackclient._request = asynctest.CoroutineMock(return_value=return_value)


def _slack_client_multiple_mock_request(slackclient, parameters):
    responses = []
    for status, body, headers in zip(
        parameters["status"], parameters["body"], parameters["headers"]
    ):
        responses.append((status, json.dumps(_fill_body(body)).encode(), headers))

    if isinstance(slackclient, SlackAPIRequest):
        slackclient._request = Mock(side_effect=responses)
    else:
        slackclient._request = asynctest.CoroutineMock(side_effect=responses)


def _expand_request_default(parameters):
    if not isinstance(parameters["status"], list):
        parameters["status"] = [parameters["status"]]
    if not isinstance(parameters["body"], list):
        parameters["body"] = [parameters["body"]]
    if not isinstance(parameters["headers"], list):
        parameters["headers"] = [parameters["headers"]]

    return parameters


def _slack_client_multiple_mock_request_with_default(slackclient, parameters):
    parameters = _expand_request_default(parameters)

    responses = list()
    for index, _ in enumerate(
        max(
            parameters["status"],
            parameters["body"],
            parameters["headers"],
            key=lambda x: len(x),
        )
    ):
        try:
            status = parameters["status"][index]
        except IndexError:
            status = parameters["status"][0]

        try:
            body = parameters["body"][index]
        except IndexError:
            body = parameters["body"][0]

        try:
            headers = parameters["headers"][index]
        except IndexError:
            headers = parameters["headers"][0]

        responses.append((status, json.dumps(_fill_body(body)).encode(), headers))

    if isinstance(slackclient, SlackAPIRequest):
        slackclient._request = Mock(side_effect=responses)
    else:
        slackclient._request = asynctest.CoroutineMock(side_effect=responses)


@pytest.fixture(params=({},))
def slack_client(request):

    parameters = _slack_client_default_parameters(request.param)
    slackclient = _slack_client(parameters)

    if all(
        isinstance(value, list)
        for value in (parameters["status"], parameters["body"], parameters["headers"],)
    ):
        _slack_client_multiple_mock_request(slackclient, parameters)
    elif any(
        isinstance(value, list)
        for value in (parameters["status"], parameters["body"], parameters["headers"],)
    ):
        _slack_client_multiple_mock_request_with_default(slackclient, parameters)
    else:
        _slack_client_single_mock_request(slackclient, parameters)

    return slackclient


def _fill_body(body):
    if isinstance(body, str):
        body = copy.deepcopy(data.Methods[body].value)
    return body


@pytest.fixture(
    params={**data.Events.__members__, **data.Messages.__members__}  # type: ignore
)
def slack_event(request):
    if isinstance(request.param, str):
        try:
            payload = copy.deepcopy(data.Events[request.param].value)
        except KeyError:
            payload = copy.deepcopy(data.Messages[request.param].value)
    else:
        payload = copy.deepcopy(request.param)

    return payload


@pytest.fixture(params={**data.Messages.__members__})  # type: ignore
def slack_message(request):
    if isinstance(request.param, str):
        payload = copy.deepcopy(data.Messages[request.param].value)
    else:
        payload = copy.deepcopy(request.param)

    return payload


@pytest.fixture()
def token():
    return copy.copy(TOKEN)


@pytest.fixture()
def itercursor():
    return "wxyz"


@pytest.fixture()
def event_router():
    return EventRouter()


@pytest.fixture()
def message_router():
    return MessageRouter()


@pytest.fixture(
    params={
        **data.InteractiveMessage.__members__,  # type: ignore
        **data.DialogSubmission.__members__,  # type: ignore
        **data.MessageAction.__members__,  # type: ignore
    }
)
def slack_action(request):
    if isinstance(request.param, str):
        try:
            payload = copy.deepcopy(data.InteractiveMessage[request.param].value)
        except KeyError:
            try:
                payload = copy.deepcopy(data.DialogSubmission[request.param].value)
            except KeyError:
                payload = copy.deepcopy(data.MessageAction[request.param].value)
    else:
        payload = copy.deepcopy(request.param)

    return payload


@pytest.fixture(params={**data.BlockAction.__members__})  # type: ignore
def block_action(request):
    return copy.deepcopy(data.BlockAction[request.param].value)


# @pytest.fixture(params={**data.InteractiveMessage.__members__})
# def interactive_message(request):
#     return Action.from_http(raw_action(request))


# @pytest.fixture(params={**data.DialogSubmission.__members__})
# def dialog_submission(request):
#     return Action.from_http(raw_action(request))


# @pytest.fixture(params={**data.MessageAction.__members__})
# def message_action(request):
#     return Action.from_http(raw_action(request))


@pytest.fixture()
def action_router():
    return ActionRouter()


@pytest.fixture(params={**data.Commands.__members__})
def slack_command(request):
    if isinstance(request.param, str):
        payload = copy.deepcopy(data.Commands[request.param].value)
    else:
        payload = copy.deepcopy(request.param)

    return payload


@pytest.fixture()
def command_router():
    return CommandRouter()
