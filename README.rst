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

0.2.1 (dev)
```````````

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
