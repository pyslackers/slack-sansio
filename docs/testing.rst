=========================================
:mod:`slack.tests.plugin` - Pytest plugin
=========================================

Slack-sansio provide a pytest plugin with some fixtures to facilitate testing of the slack API.

To load the plugin add the snippet below to your ``conftest.py``.

.. code-block:: python

    pytest_plugins = "slack.tests.plugin",


The ``slack_actions``, ``slack_commands`` and ``slack_events`` fixtures return sample of incoming actions, commands or
events coming from slack.

.. code-block:: python

    async def test_event(self, slack_event):
        event = slack.events.Event.from_http(slack_event)

