==========================================
:mod:`slack.io.trio` - Trio implementation
==========================================

.. module:: slack.io.trio

.. autoclass:: slack.io.trio.SlackAPI
   :members:
   :inherited-members:
   :exclude-members: iter, rtm

   .. autocomethod:: iter
      :async-for:

.. _trio-examples:

Examples
--------

Query
^^^^^

.. literalinclude:: ../../examples/trio/query.py

Iterate
^^^^^^^

.. literalinclude:: ../../examples/trio/iterate.py
