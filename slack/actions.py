import json
import typing
import logging
from typing import Any, Dict, Iterator, Optional
from collections import defaultdict
from collections.abc import MutableMapping

from . import exceptions

LOG = logging.getLogger(__name__)


class Action(MutableMapping):
    """
    MutableMapping representing a response to an interactive message, a dialog submission or a message action.

    Args:
        raw_action: Decoded body of the HTTP request
        verification_token: Slack verification token used to verify the request came from slack
        team_id: Verify the event is for the correct team
    Raises:
        :class:`slack.exceptions.FailedVerification`: when `verification_token` or `team_id` does not match the
                                                      incoming event's
    """

    def __init__(
        self,
        raw_action: typing.MutableMapping,
        verification_token: Optional[str] = None,
        team_id: Optional[str] = None,
    ) -> None:
        self.action = raw_action

        if verification_token and self.action["token"] != verification_token:
            raise exceptions.FailedVerification(
                self.action["token"], self.action["team"]["id"]
            )

        if team_id and self.action["team"]["id"] != team_id:
            raise exceptions.FailedVerification(
                self.action["token"], self.action["team"]["id"]
            )

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

    @classmethod
    def from_http(
        cls,
        payload: typing.MutableMapping,
        verification_token: Optional[str] = None,
        team_id: Optional[str] = None,
    ) -> "Action":
        action = json.loads(payload["payload"])
        return cls(action, verification_token=verification_token, team_id=team_id)


class Router:
    """
    When creating a slack applications you can only set one action url. This provide a routing mechanism for the
    incoming actions, based on their `callback_id` and the action name, to one or more handlers.
    """

    def __init__(self):
        self._routes: Dict[str, Dict] = defaultdict(dict)

    def register(self, callback_id: str, handler: Any, name: str = "*") -> None:
        """
        Register a new handler for a specific :class:`slack.actions.Action` `callback_id`.
        Optional routing based on the action name too.

        The name argument is useful for actions of type `interactive_message` to provide
        a different handler for each individual action.

        Args:
            callback_id: Callback_id the handler is interested in
            handler: Callback
            name: Name of the action (optional).
        """
        LOG.info("Registering %s, %s to %s", callback_id, name, handler)
        if name not in self._routes[callback_id]:
            self._routes[callback_id][name] = []

        self._routes[callback_id][name].append(handler)

    def dispatch(self, action: Action) -> Any:
        """
        Yields handlers matching the incoming :class:`slack.actions.Action` `callback_id`.

        Args:
            action: :class:`slack.actions.Action`

        Yields:
            handler
        """
        LOG.debug("Dispatching action %s, %s", action["type"], action["callback_id"])

        if action["type"] == "interactive_message":
            yield from self._dispatch_interactive_message(action)
        elif action["type"] in ("dialog_submission", "message_action"):
            yield from self._dispatch_action(action)
        else:
            raise UnknownActionType(action)

    def _dispatch_action(self, action: Action) -> Iterator[Any]:
        yield from self._routes[action["callback_id"]].get("*", [])

    def _dispatch_interactive_message(self, action: Action) -> Iterator[Any]:
        if action["actions"][0]["name"] in self._routes[action["callback_id"]]:
            yield from self._routes[action["callback_id"]][action["actions"][0]["name"]]
        else:
            yield from self._routes[action["callback_id"]].get("*", [])


class UnknownActionType(Exception):
    """
    Raised for incoming action with unknown type

    Attributes:
        action: The incoming action
    """

    def __init__(self, action: Action) -> None:
        self.action = action
