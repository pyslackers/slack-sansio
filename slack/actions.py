import logging

from collections import defaultdict, MutableMapping
from . import exceptions

LOG = logging.getLogger(__name__)


class Action(MutableMapping):
    """
    MutableMapping representing a response to an interactive message.

    Args:
        raw_action: Decoded body of the HTTP request
        verification_token: Slack verification token used to verify the request came from slack
        team_id: Verify the event is for the correct team
    Raises:
        :class:`slack.exceptions.FailedVerification`: when `verification_token` or `team_id` does not match the
                                                      incoming event's
    """

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
    """
    When creating a slack applications you can only set one action url. This provide a routing mechanism for the
    incoming actions, based on their `callback_id`, to one or more handlers.
    """
    def __init__(self):
        self._routes = defaultdict(dict)

    def register(self, callback_id, handler):
        """
        Register a new handler for a specific :class:`slack.actions.Action` `callback_id`.

        Args:
            callback_id: Callback_id the handler is interested in
            handler: Callback
        """
        LOG.info('Registering %s to %s', callback_id, handler.__name__)
        self._routes[callback_id].append(handler)

    def dispatch(self, action):
        """
        Yields handlers matching the incoming :class:`slack.actions.Action` `callback_id`.

        Args:
            action: :class:`slack.actions.Action`

        Yields:
            handler
        """
        LOG.debug('Dispatching action %s', action['callback_id'])

        for callback in self._routes.get(action['callback_id']):
            yield callback
