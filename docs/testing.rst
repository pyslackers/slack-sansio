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

.. automodule:: slack.tests.plugin
   :members:


Available data
==============

.. autoclass:: slack.tests.data.Events
   :members:

.. autoclass:: slack.tests.data.Messages
   :members:

.. autoclass:: slack.tests.data.Commands
   :members:

.. autoclass:: slack.tests.data.Actions
   :members:

.. autoclass:: slack.tests.data.Methods
   :members:
