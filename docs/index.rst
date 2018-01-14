====================================================
slack-sansio | (a)sync library for using Slack's API
====================================================

This projects aims to provide a simple library that abstract the slack API details.

Many slack libraries already exist for Python but none oriented towards asynchronous usage. While working on
`Sir bot-a-lot <https://github.com/pyslackers/sir-bot-a-lot>`_ we figured the slack client could be useful for the
community and decided to take it out and create this library. We also choose to take a
`sans-I/O approach <https://sans-io.readthedocs.io/>`_ to allow reusability for other asynchronous frameworks.

I/O Implementations
-------------------

Most people would want to use one of these implementations directly. For those that have an HTTP library which is not
supported this library provide the base tools to ease the use of the Slack API.

 - Synchronous with `request <http://docs.python-requests.org>`_.
 - `Asyncio <https://docs.python.org/3/library/asyncio.html>`_ with `aiohttp <http://aiohttp.readthedocs.io/en/stable/>`_.

In development
^^^^^^^^^^^^^^

 - `Curio <http://curio.readthedocs.io>`_ with `asks <http://asks.readthedocs.io>`_.
 - `Trio <http://trio.readthedocs.io/>`_ with `asks <http://asks.readthedocs.io>`_.
 - `Twisted <https://twistedmatrix.com/trac/>`_ with `treq <https://github.com/twisted/treq>`_.

Installation
------------

`slack-sansio is on PyPI <https://pypi.python.org/pypi/slack-sansio>`_

.. code:: console

    $ pip3 install slack-sansio  # No extra requirements

Due to it's sans-I/O approach extra requirements are needed for each implementations. You can install them with:

.. code:: console

    $ pip3 install slack-sansio[requests] # requests implementation extra requirements
    $ pip3 install slack-sansio[aiohttp]  # aiohttp implementation extra requirements
    $ pip3 install slack-sansio[curio]    # curio implementation extra requirements
    $ pip3 install slack-sansio[trio]     # trio implementation extra requirements
    $ pip3 install slack-sansio[treq]     # treq implementation extra requirements
    $ pip3 install slack-sansio[full]     # all implementations extra requirements

Examples
--------

Examples are dependant of the implementations and can be found on the documentation of each implementation.

 - :ref:`Requests examples <requests-examples>`
 - :ref:`Aiohttp examples <aiohttp-examples>`
 - :ref:`Curio examples <curio-examples>`
 - :ref:`Trio examples <trio-examples>`
 - :ref:`Treq examples <treq-examples>`

Methods
-------

For ease of use the library provide an :py:class:`enum.Enum` of all the slack API methods.

.. module:: slack.methods

.. autoclass:: slack.methods
   :noindex:

.. autoclass:: slack.methods.Methods
   :members:


Navigation
----------

.. toctree::
   :maxdepth: 1

   events
   commands
   actions
   implementations/abc
   implementations/requests
   implementations/aiohttp
   implementations/curio
   implementations/trio
   implementations/treq
   sansio
   exceptions
   testing
