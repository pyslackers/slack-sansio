====================================================
slack-sansio | (a)sync library for using Slack's API
====================================================

This projects aims to provide a simple library that abstract the slack API details.

Many slack libraries already exist for Python but none oriented towards asynchronous usage. While working on
`Sir bot-a-lot <https://github.com/pyslackers/sir-bot-a-lot>`_ we figured the slack client could be useful for the
community and decided to take it out and create this library. We also choose to take a
`sans-I/O approach <https://sans-io.readthedocs.io/>`_ to allow reusability for other asynchronous frameworks.

This library also provide two implementation, one synchronous built upon
`request <http://docs.python-requests.org/en/master/>`_  and a second one asynchronous built upon
`aiohttp <http://aiohttp.readthedocs.io/en/stable/>`_. Most people would want to use one of these implementations.
For those that have an HTTP library which is not supported this library provide the base tools to ease the use of the
Slack API.

Installation
------------

`slack-sansio is on PyPI <https://pypi.python.org/pypi/slack-sansio>`_

.. code:: console

    $ pip3 install slack-sansio  # No extra requirements

Due to it's sans-I/O approach extra requirements are needed for each implementations. You can install them with:

.. code:: console

    $ pip3 install slack-sansio[requests]  # requests implementation extra requirements
    $ pip3 install slack-sansio[aiohttp]  # aiohttp implementation extra requirements
    $ pip3 install slack-sansio[full]  # all implementations extra requirements

Examples
--------

Examples are dependant of the implementations and can be found on the documentation of each implementation.

 - :ref:`Requests examples <requests-examples>`
 - :ref:`Aiohttp examples <aiohttp-examples>`

Navigation
----------

.. toctree::
   :maxdepth: 1

   methods
   exceptions
   events
   implementations/abc
   implementations/requests
   implementations/aiohttp
