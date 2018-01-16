import pytest

from . import data
from .conftest import raw_event
from .conftest import raw_action
from .conftest import raw_command
from .conftest import client, FakeIO


@pytest.fixture(params={**data.Events.__members__, **data.Messages.__members__})
def slack_event(request):
    """
    Fixture returning data sent by the slack event API.

    This fixture can be parametrized to return one or more available event from :class:`slack.tests.data.Events`
    and :class:`slack.tests.data.Messages`.

    .. code:: python

        @pytest.mark.parametrize('slack_event', ('channel_deleted', 'simple'), indirect=True)
        def test_events(slack_event):
            assert True
    """
    return raw_event(request)


@pytest.fixture(params={**data.Events.__members__})
def slack_event_only(request):
    """
    Fixture returning data sent by the slack event API of any type except ``message``.
    """
    return raw_event(request)


@pytest.fixture(params={**data.Messages.__members__})
def slack_message(request):
    """
    Fixture returning data sent by the slack event API of type ``message``.
    """
    return raw_event(request)


@pytest.fixture(params={**data.Actions.__members__})
def slack_action(request):
    """
    Fixture returning data sent by the slack API when using an interactive message.

    This fixture can be parametrized to return one or more available action from :class:`slack.tests.data.Actions`.

    .. code:: python

        @pytest.mark.parametrize('slack_action', ('button_ok', 'button_cancel'), indirect=True)
        def test_actions(slack_action):
            assert True
    """
    return raw_action(request)


@pytest.fixture(params={**data.Commands.__members__})
def slack_command(request):
    """
    Fixture returning data sent by the slack API when using a slash command.

    This fixture can be parametrized to return one or more available command from :class:`slack.tests.data.Commands`.

    .. code:: python

        @pytest.mark.parametrize('slack_command', ('text', 'no_text'), indirect=True)
        def test_commands(slack_command):
            assert True
    """
    return raw_command(request)


@pytest.fixture()
def slack_client(request):
    """
    Fixture returning a fake slack client.

    By default the client return to any request:
        - status: ``200``
        - body: ``{'ok': True}``
        - headers: ``{'content-type': 'application/json; charset=utf-8'}``

    This can be parametrize with the ``_request`` parameter.

    .. code:: python

        @pytest.mark.asyncio
        @pytest.mark.parametrize('slack_client', ({'_request': {'body': {'ok': True, 'hello': 'world'}}},),
         indirect=True)
        async def test_client(slack_client):
            data = await slack_client.query(slack.methods.AUTH_TEST)
            assert data == {'ok': True, 'hello': 'world'}

    The ``body`` parameter of a request can be a string corresponding to one of the methods available
    in :class:`slack.tests.data.Methods`.

    For multiple requests you can set the ``_request`` parameter to a ``list``.

    .. code:: python

        @pytest.mark.asyncio
        @pytest.mark.parametrize('slack_client', ({'_request': [
            {'body': 'channels'},
            {'status': 500}
        ]},), indirect=True)
        async def test_client(slack_client):
            data1 = await slack_client.query(slack.methods.AUTH_TEST)
            with pytest.raises(slack.exceptions.HTTPException):
                await slack_client.query(slack.methods.AUTH_TEST)
    """
    return client(request, io_client=FakeIO)
