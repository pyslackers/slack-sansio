import logging

from collections import defaultdict, MutableMapping
from . import exceptions

LOG = logging.getLogger(__name__)


class Action(MutableMapping):

    def __init__(self, raw_action, verification_token=None, team_id=None):
        self.action = raw_action

        if verification_token and self.action['token'] != verification_token:
            raise exceptions.FailedVerification(self.action['token'], self.action['team_id'])

        if team_id and self.action['team_id'] != team_id:
            raise exceptions.FailedVerification(self.action['token'], self.action['team_id'])

    def __getitem__(self, item):
        return self.action[item]

    def __setitem__(self, key, value):
        self.action[key] = value

    def __delitem__(self, key):
        del self.action[key]

    def __iter__(self):
        return iter(self.action)

    def __len__(self):
        return len(self.action)

    def __repr__(self):
        return str(self.action)


class Router:

    def __init__(self):
        self._routes = defaultdict(dict)

    def register(self, callback_id, handler):
        LOG.info('Registering %s to %s', callback_id, handler.__name__)
        self._routes[callback_id].append(handler)

    def dispatch(self, action):
        LOG.debug('Dispatching action %s', action['callback_id'])

        try:
            for callback in self._routes[action['callback_id']]:
                yield callback
        except KeyError:
            raise exceptions.UnknownAction(action)
