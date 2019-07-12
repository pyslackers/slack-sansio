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

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST EVENTS
        :end-before: # END: TEST EVENTS

    To only get :class:`slack.tests.data.Messages` members you can parametrize the test that way:

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST MESSAGES
        :end-before: # END: TEST MESSAGES


.. function:: slack.tests.plugin.slack_action

    Fixture returning data sent by the slack API when using an interactive message or dialog.

    This fixture can be parametrized to return one or more available action
    from :class:`slack.tests.data.InteractiveMessage` or :class:`slack.tests.data.DialogSubmission`.

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST ACTIONS
        :end-before: # END: TEST ACTIONS


.. function:: slack.tests.plugin.slack_command

    Fixture returning data sent by the slack API when using a slash command.

    This fixture can be parametrized to return one or more available command from :class:`slack.tests.data.Commands`.

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST COMMANDS
        :end-before: # END: TEST COMMANDS


.. function:: slack.tests.plugin.slack_client

    Fixture returning a fake slack client.

    By default the client return to any request:
        - status: ``200``
        - body: ``{'ok': True}``
        - headers: ``{'content-type': 'application/json; charset=utf-8'}``

    Parametrize a reponse:

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST CLIENT CUSTOM BODY
        :end-before: # END: TEST CLIENT CUSTOM BODY

    The ``body`` parameter of a request can be a string corresponding to one of the methods available
    in :class:`slack.tests.data.Methods`.

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST CLIENT BODY
        :end-before: # END: TEST CLIENT BODY

    Parametrize multiple responses:

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST CLIENT STATUS
        :end-before: # END: TEST CLIENT STATUS

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST CLIENT ITER
        :end-before: # END: TEST CLIENT ITER

    Parametrize multiple run:

    .. literalinclude:: ../slack/tests/test_examples.py
        :start-after: # START: TEST CLIENT MULTIPLE RUN
        :end-before: # END: TEST CLIENT MULTIPLE RUN


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
