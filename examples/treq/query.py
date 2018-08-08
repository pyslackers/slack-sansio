import os
import sys
import pprint
import logging

from twisted.internet import task, defer, reactor
import slack
from slack.io.treq import SlackAPI

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def main(reactor):
    client = SlackAPI(token=TOKEN)
    d = defer.ensureDeferred(client.query(slack.methods.AUTH_TEST))
    d.addCallback(pprint.pprint)
    return d


if __name__ == "__main__":

    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.environ.get("SLACK_TOKEN")

    if not TOKEN:
        raise ValueError("No slack token provided !")

    task.react(main)
