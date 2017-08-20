============================================
:mod:`slack.io.curio` - Curio implementation
============================================

.. module:: slack.io.curio

.. autoclass:: slack.io.curio.SlackAPI
   :members:
   :inherited-members:
   :exclude-members: iter, rtm

   .. autocomethod:: iter
      :async-for:

.. _curio-examples:

Examples
--------

Query
^^^^^

.. literalinclude:: ../../examples/curio/query.py

Iterate
^^^^^^^

.. literalinclude:: ../../examples/curio/iterate.py
