slack-sansio
============

Python (a)sync `Slack API <https://api.slack.com/>`_ library

.. image:: https://travis-ci.org/pyslackers/slack-sansio.svg?branch=master
    :target: https://travis-ci.org/pyslackers/slack-sansio

Installation
------------

Slack-sansio is `available on PyPI <https://pypi.org/project/slack-sansio/>`_.

.. code::

    $ pip3 install slack-sansio  # No specific implementation requirements
    $ pip3 install slack-sansio[requests]  # Requests implementation requirements
    $ pip3 install slack-sansio[aiohttp]  # Aiohttp implementation requirements
    $ pip3 install slack-sansio[full]  # All implementations requirements

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

I/O Implementation
------------------

Two I/O implementation are provided with the library. One synchronous built upon
`request <http://docs.python-requests.org/en/master/>`_  and a second one built upon
`aiohttp <http://aiohttp.readthedocs.io/en/stable/>`_.

The library also provide an abstract base class on which to built I/O implementation.

Changelog
---------

0.1.0
`````

* Initial beta release
* RTM API
* Pagination

0.0.1
`````

* Initial development release
