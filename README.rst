`slack-sansio <http://slack-sansio.readthedocs.io>`_
====================================================

Python (a)sync `Slack API <https://api.slack.com/>`_ library

.. image:: https://readthedocs.org/projects/slack-sansio/badge/?version=stable
    :target: http://slack-sansio.readthedocs.io/en/stable/?badge=stable
    :alt: Documentation Status
.. image:: https://travis-ci.org/pyslackers/slack-sansio.svg?branch=master
    :target: https://travis-ci.org/pyslackers/slack-sansio
    :alt: Travis-ci status
.. image:: https://badge.fury.io/py/slack-sansio.svg
    :target: https://pypi.org/project/slack-sansio/
    :alt: PyPI status
.. image:: https://coveralls.io/repos/github/pyslackers/slack-sansio/badge.svg?branch=master
    :target: https://coveralls.io/github/pyslackers/slack-sansio?branch=master
    :alt: Coverage status

Installation
------------

Slack-sansio is `available on PyPI <https://pypi.org/project/slack-sansio/>`_.

.. code::

    $ pip3 install slack-sansio  # No specific implementation requirements

.. code::

    $ pip3 install slack-sansio[requests]   # Requests implementation requirements
    $ pip3 install slack-sansio[aiohttp]    # Aiohttp implementation requirements
    $ pip3 install slack-sansio[curio]      # Curio implementation requirements
    $ pip3 install slack-sansio[trio]       # Trio implementation requirements
    $ pip3 install slack-sansio[treq]       # Treq implementation requirements
    $ pip3 install slack-sansio[full]       # All implementations requirements

Quickstart
----------

.. code-block:: python

    import slack
    import pprint
    import requests

    from slack.io.sync import SlackAPI

    session = requests.session()
    slack_client = SlackAPI(token=TOKEN, session=session)
    data = client.query(slack.methods.AUTH_TEST)
    pprint.pprint(data)

For more examples see the `examples folder <https://github.com/pyslackers/slack-sansio/tree/master/examples>`_.

I/O Implementations
-------------------

Most people would want to use one of these implementations directly. For those that have an HTTP library which is not
supported this library provide the base tools to ease the use of the Slack API.

* Synchronous with `request <http://docs.python-requests.org>`_.
* `Asyncio <https://docs.python.org/3/library/asyncio.html>`_ with `aiohttp <http://aiohttp.readthedocs.io/en/stable/>`_.

* `Curio <http://curio.readthedocs.io>`_ with `asks <http://asks.readthedocs.io>`_ (In development).
* `Trio <http://trio.readthedocs.io/>`_ with `asks <http://asks.readthedocs.io>`_ (In development).
* `Twisted <https://twistedmatrix.com/trac/>`_ with `treq <https://github.com/twisted/treq>`_ (In development).

The library also provide an abstract base class on which to built I/O implementation.

Changelog
---------

dev
```

0.3.5
`````

* Add ``subtype`` argument to ``events.MessageRouter.register``.
* Fix routing bug for message with ``text=None``.

0.3.4
`````

* Refactor tests
* Create pytest plugin with useful fixtures.


0.3.3
`````

* Add ``minimum_time`` argument to ``SlackAPI.iter`` in order to force a minimum elapsed time between two call to the API

0.3.2
`````

* Add conversation & dialog methods in Enum.
* Fix ``not_authed`` when using rate limit retry.

0.3.1
`````

* Bugfix for ``actions.Action`` and ``actions.Router``.
* Bugfix in data serialization for response urls ``https://hooks.slack.com/``.

0.3.0
`````

* Bugfix for ``commands.Router``.
* New ``events.MessageRouter`` for ``events.Message`` routing based on regular expression.
* Rename ``events.Router`` to ``events.EventRouter``.
* Change ``TypeError`` to ``ValueError`` in ``events.EventRouter.register``.
* Bugfix for threaded messages.

0.2.2
`````

* Fix routing bug in ``events.Router``.
* Inherit from ``Exception`` instead of ``BaseExecption`` in custom exceptions.

0.2.1
`````

* Curio support (query and iterate)
* Trio support (query and iterate)
* Twisted support (query only)

0.2.0
`````

* Enum of slack API methods

0.1.0
`````

* Initial beta release
* RTM API
* Pagination

0.0.1
`````

* Initial development release
