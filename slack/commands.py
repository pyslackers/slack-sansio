import logging

from collections import defaultdict, MutableMapping
from . import exceptions

LOG = logging.getLogger(__name__)


class Command(MutableMapping):
    """
    MutableMapping representing a slack slash command.

    Args:
        raw_command: Decoded body of the webhook HTTP request

    Raises:
        :class:`slack.exceptions.FailedVerification`: when `verification_token` or `team_id` does not match the
                                                      incoming command's
    """

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
    """
    When creating slash command for your applications each one can have a custom webhook url. For ease of configuration
    this class provide a routing mechanisms based on the command so that each command can define the same webhook
    url.
    """
    def __init__(self):
        self._routes = defaultdict(list)

    def register(self, command, handler):
        """
        Register a new handler for a specific slash command

        Args:
            command: Slash command
            handler: Callback
        """

        if not command.startswith('/'):
            command = f'/{command}'

        LOG.info('Registering %s to %s', command, handler)
        self._routes[command].append(handler)

    def dispatch(self, command):
        """
        Yields handlers matching the incoming :class:`slack.actions.Command`.

        Args:
            command: :class:`slack.actions.Command`

        Yields:
            handler
        """
        LOG.debug('Dispatching command %s', command['command'])
        for callback in self._routes[command['command']]:
            yield callback
