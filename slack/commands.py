import logging

from collections import defaultdict, MutableMapping
from . import exceptions

LOG = logging.getLogger(__name__)


class Command(MutableMapping):

    def __init__(self, raw_command, verification_token=None, team_id=None):
        self.command = raw_command

        if verification_token and self.command['token'] != verification_token:
            raise exceptions.FailedVerification(self.command['token'], self.command['team_id'])

        if team_id and self.command['team_id'] != team_id:
            raise exceptions.FailedVerification(self.command['token'], self.command['team_id'])

    def __getitem__(self, item):
        return self.command[item]

    def __setitem__(self, key, value):
        self.command[key] = value

    def __delitem__(self, key):
        del self.command[key]

    def __iter__(self):
        return iter(self.command)

    def __len__(self):
        return len(self.command)

    def __repr__(self):
        return str(self.command)


class Router:

    def __init__(self):
        self._routes = defaultdict(dict)

    def register(self, command, handler):
        LOG.info('Registering %s to %s', command, handler.__name__)
        self._routes[command].append(handler)

    def dispatch(self, command):
        LOG.debug('Dispatching command %s', command['command'])
        for callback in self._routes[command['command']]:
            yield callback
