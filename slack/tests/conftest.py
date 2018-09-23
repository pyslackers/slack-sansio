import copy
import json
import time
import functools
from unittest.mock import Mock

import pytest
import requests
import asynctest
from slack.events import Event, EventRouter, MessageRouter
from slack.io.abc import SlackAPI
from slack.actions import Action
from slack.actions import Router as ActionRouter
from slack.commands import Router as CommandRouter
from slack.commands import Command

from . import data

try:
    from slack.io.requests import SlackAPI as SlackAPIRequest
except ImportError:
    SlackAPIRequest = None  # type: ignore


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


@pytest.fixture(params=(FakeIO,))
def io_client(request):
    return request.param


@pytest.fixture(params=({"token": TOKEN},))
def client(request, io_client):
    default_request = {
        "status": 200,
        "body": {"ok": True},
        "headers": {"content-type": "application/json; charset=utf-8"},
    }

    if "_request" not in request.param:
        request.param["_request"] = default_request
    elif isinstance(request.param["_request"], dict):
        request.param["_request"] = _default_response(request.param["_request"])
    elif isinstance(request.param["_request"], list):
        for index, item in enumerate(request.param["_request"]):
            request.param["_request"][index] = _default_response(item)
    else:
        raise ValueError("Invalid `_request` parameters: %s", request.param["_request"])

    if "token" not in request.param:
        request.param["token"] = TOKEN

    slackclient = io_client(
        **{k: v for k, v in request.param.items() if not k.startswith("_")}
    )

    if isinstance(request.param["_request"], dict):
        return_value = (
            request.param["_request"]["status"],
            json.dumps(request.param["_request"]["body"]).encode(),
            request.param["_request"]["headers"],
        )
        if isinstance(slackclient, SlackAPIRequest):
            slackclient._request = Mock(return_value=return_value)
        else:
            slackclient._request = asynctest.CoroutineMock(return_value=return_value)
    else:
        responses = [
            (
                response["status"],
                json.dumps(response["body"]).encode(),
                response["headers"],
            )
            for response in request.param["_request"]
        ]
        if isinstance(slackclient, SlackAPIRequest):
            slackclient._request = Mock(side_effect=responses)
        else:
            slackclient._request = asynctest.CoroutineMock(side_effect=responses)

    return slackclient


def _default_response(response):
    default_response = {
        "status": 200,
        "body": {"ok": True},
        "headers": {"content-type": "application/json; charset=utf-8"},
    }
    response = {**default_response, **response}
    if "content-type" not in response["headers"]:
        response["headers"]["content-type"] = default_response["headers"][
            "content-type"
        ]
    if isinstance(response["body"], str):
        response["body"] = copy.deepcopy(data.Methods[response["body"]].value)
    return response


@pytest.fixture(
    params={**data.Events.__members__, **data.Messages.__members__}  # type: ignore
)
def event(request):
    if isinstance(request.param, str):
        try:
            payload = copy.deepcopy(data.Events[request.param].value)
        except KeyError:
            payload = copy.deepcopy(data.Messages[request.param].value)
    else:
        payload = copy.deepcopy(request.param)

    return payload


@pytest.fixture(params={**data.Messages.__members__})  # type: ignore
def message(request):
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
def action(request):
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
def command(request):
    if isinstance(request.param, str):
        payload = copy.deepcopy(data.Commands[request.param].value)
    else:
        payload = copy.deepcopy(request.param)

    return payload


@pytest.fixture()
def command_router():
    return CommandRouter()
