================================================
:mod:`slack.io.aiohttp` - Aiohttp implementation
================================================

.. module:: slack.io.aiohttp

.. autoclass:: slack.io.aiohttp.SlackAPI
   :members:
   :inherited-members:
   :exclude-members: iter, rtm

   .. autocomethod:: iter
      :async-for:

   .. autocomethod:: rtm
      :async-for:

.. _aiohttp-examples:

Examples
--------

Query
^^^^^

.. literalinclude:: ../../examples/aiohttp/query.py

Iterate
^^^^^^^

.. literalinclude:: ../../examples/aiohttp/iterate.py

RTM
^^^

.. literalinclude:: ../../examples/aiohttp/rtm.py
