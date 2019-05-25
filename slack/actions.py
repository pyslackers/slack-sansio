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

    def register_interactive_message(
        self, callback_id: str, handler: Any, name: str = "*"
    ) -> None:
        """
        Register a new handler for a specific :class:`slack.actions.Action` `callback_id`.
        Optional routing based on the action name too.

        The name argument is useful for actions of type `interactive_message` to provide
        a different handler for each individual action.

        Internally calls the base :meth:`register<slack.actions.Router.register>` method for
        actual registration.

        Args:
            callback_id: Callback_id the handler is interested in
            handler: Callback
            name: Name of the action (optional).
        """
        self.register(callback_id, handler, name)

    def register_block_action(
        self, block_id: str, handler: Any, action_id: str = "*"
    ) -> None:
        """
        Register a new handler for a block-based :class:`slack.actions.Action`.
        Internally uses the base `register` method for actual registration.

        Optionally provides routing based on a specific `action_id` if present.

        Args:
            block_id: The action block_id the handler is interested in
            handler: Callback
            action_id: specific action_id for the action (optional)
        """
        self.register(block_id, handler, action_id)

    def register_dialog_submission(self, callback_id: str, handler: Any):
        """
        Registers a new handler for a `dialog_submission` :class:`slack.actions.Action`.

        Internally calls the base :meth:`register<slack.actions.Router.register>` method for
        actual registration.

        Args:
            callback_id: Callback_id the handler is interested in
            handler: Callback
        """
        self.register(callback_id, handler)

    def dispatch(self, action: Action) -> Any:
        """
        Yields handlers matching the incoming :class:`slack.actions.Action` `callback_id` or `action_id`.

        Args:
            action: :class:`slack.actions.Action`

        Yields:
            handler
        """
        if "callback_id" in action:
            LOG.debug(
                "Dispatching action %s, %s", action["type"], action["callback_id"]
            )
        else:
            LOG.debug(
                "Dispatching action %s, %s",
                action["actions"][0]["type"],
                action["actions"][0]["action_id"],
            )

        if action["type"] == "interactive_message":
            yield from self._dispatch_interactive_message(action)
        elif action["type"] in ("dialog_submission", "message_action"):
            yield from self._dispatch_action(action)
        elif action["type"] == "block_actions":
            yield from self._dispatch_block_actions(action)
        else:
            raise UnknownActionType(action)

    def _dispatch_action(self, action: Action) -> Iterator[Any]:
        yield from self._routes[action["callback_id"]].get("*", [])

    def _dispatch_interactive_message(self, action: Action) -> Iterator[Any]:
        if action["actions"][0]["name"] in self._routes[action["callback_id"]]:
            yield from self._routes[action["callback_id"]][action["actions"][0]["name"]]
        else:
            yield from self._routes[action["callback_id"]].get("*", [])

    def _dispatch_block_actions(self, action: Action) -> Iterator[Any]:
        block_id = action["actions"][0]["block_id"]
        action_id = action["actions"][0].get("action_id", "*")

        if action_id in self._routes[block_id]:
            yield from self._routes[block_id].get(action_id, [])
        else:
            yield from self._routes[block_id].get("*", [])


class UnknownActionType(Exception):
    """
    Raised for incoming action with unknown type

    Attributes:
        action: The incoming action
    """

    def __init__(self, action: Action) -> None:
        self.action = action
