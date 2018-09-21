===========================================
:mod:`slack.tests.plugin` - Pytest fixtures
===========================================

Slack-sansio provide a pytest plugin with some fixtures to facilitate testing of the slack API.


Installation
============

To load the plugin add the snippet below to your ``conftest.py``.

.. code-block:: python

    pytest_plugins = "slack.tests.plugin",


Available fixtures
==================

.. function:: slack.tests.plugin.slack_event

    Fixture returning data sent by the slack event API.

    This fixture can be parametrized to return one or more available event from :class:`slack.tests.data.Events`
    and :class:`slack.tests.data.Messages`.

    .. code:: python

        @pytest.mark.parametrize('slack_event', ('channel_deleted', 'simple'), indirect=True)
        def test_events(slack_event):
            assert True

    To only get :class:`slack.tests.data.Messages` members you can parametrize the test that way:

    .. code:: python

        @pytest.mark.parametrize("slack_event", {**slack.tests.data.Messages.__members__}, indirect=True)
        async def test_messages(self, slack_event):
            assert slack_event["event"]["type"] == "message"


.. function:: slack.tests.plugin.slack_action

    Fixture returning data sent by the slack API when using an interactive message or dialog.

    This fixture can be parametrized to return one or more available action
    from :class:`slack.tests.data.InteractiveMessage` or :class:`slack.tests.data.DialogSubmission`.

    .. code:: python

        @pytest.mark.parametrize('slack_action', ('button_ok', 'button_cancel'), indirect=True)
        def test_actions(slack_action):
            assert True


.. function:: slack.tests.plugin.slack_command

    Fixture returning data sent by the slack API when using a slash command.

    This fixture can be parametrized to return one or more available command from :class:`slack.tests.data.Commands`.

    .. code:: python

        @pytest.mark.parametrize('slack_command', ('text', 'no_text'), indirect=True)
        def test_commands(slack_command):
            assert True


.. function:: slack.tests.plugin.slack_client

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

Available data
==============

.. autoclass:: slack.tests.data.Events
   :members:

.. autoclass:: slack.tests.data.Messages
   :members:

.. autoclass:: slack.tests.data.Commands
   :members:

.. autoclass:: slack.tests.data.InteractiveMessage
   :members:

.. autoclass:: slack.tests.data.DialogSubmission
   :members:

.. autoclass:: slack.tests.data.Methods
   :members:
