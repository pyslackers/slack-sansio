import re
import json
import copy
import logging
import itertools

from collections import defaultdict, MutableMapping

from . import exceptions

LOG = logging.getLogger(__name__)


class Event(MutableMapping):
    """
    MutableMapping representing a slack event coming from the RTM API or the Event API.

    Attributes:
        metadata: Metadata dispatched with the event when using the Event API
                  (see `slack event API documentation <https://api.slack.com/events-api#receiving_events>`_)
    """

    def __init__(self, raw_event, metadata=None):
        self.event = raw_event
        self.metadata = metadata

    def __getitem__(self, item):
        return self.event[item]

    def __setitem__(self, key, value):
        self.event[key] = value

    def __delitem__(self, key):
        del self.event[key]

    def __iter__(self):
        return iter(self.event)

    def __len__(self):
        return len(self.event)

    def __repr__(self):
        return 'Slack Event: ' + str(self.event)

    def clone(self):
        """
        Clone the event

        Returns:
            :class:`slack.events.Event`

        """
        return self.__class__(copy.deepcopy(self.event), copy.deepcopy(self.metadata))

    @classmethod
    def from_rtm(cls, raw_event):
        """
        Create an event with data coming from the RTM API.

        If the event type is a message a :class:`slack.events.Message` is returned.

        Args:
            raw_event: JSON decoded data from the RTM API

        Returns:
            :class:`slack.events.Event` or :class:`slack.events.Message`
        """
        if raw_event['type'].startswith('message'):
            return Message(raw_event)
        else:
            return Event(raw_event)

    @classmethod
    def from_http(cls, raw_body, verification_token=None, team_id=None):
        """
        Create an event with data coming from the HTTP Event API.

        If the event type is a message a :class:`slack.events.Message` is returned.

        Args:
            raw_body: Decoded body of the Event API request
            verification_token: Slack verification token used to verify the request came from slack
            team_id: Verify the event is for the correct team

        Returns:
            :class:`slack.events.Event` or :class:`slack.events.Message`

        Raises:
            :class:`slack.exceptions.FailedVerification`: when `verification_token` or `team_id` does not match the
                                                          incoming event's.
        """
        if verification_token and raw_body['token'] != verification_token:
            raise exceptions.FailedVerification(raw_body['token'], raw_body['team_id'])

        if team_id and raw_body['team_id'] != team_id:
            raise exceptions.FailedVerification(raw_body['token'], raw_body['team_id'])

        if raw_body['event']['type'].startswith('message'):
            return Message(raw_body['event'], metadata=raw_body)
        else:
            return Event(raw_body['event'], metadata=raw_body)


class Message(Event):
    """
    Type of :class:`slack.events.Event` corresponding to a message event type
    """

    def __init__(self, msg=None, metadata=None):
        if not msg:
            msg = {}
        super().__init__(msg, metadata)

    def __repr__(self):
        return 'Slack Message: ' + str(self.event)

    def response(self, in_thread=None):
        """
        Create a response message.

        Depending on the incoming message the response can be in a thread. By default the response follow where the
        incoming message was posted.

        Args:
            in_thread (boolean): Overwrite the `threading` behaviour

        Returns:
             a new :class:`slack.event.Message`
        """
        data = {'channel': self['channel']}

        if in_thread:
            if 'message' in self:
                data['thread_ts'] = self['message'].get('thread_ts') or self['message']['ts']
            else:
                data['thread_ts'] = self.get('thread_ts') or self['ts']
        elif in_thread is None:
            if 'message' in self and 'thread_ts' in self['message']:
                data['thread_ts'] = self['message']['thread_ts']
            elif 'thread_ts' in self:
                data['thread_ts'] = self['thread_ts']

        return Message(data)

    def serialize(self):
        """
        Serialize the message for sending to slack API

        Returns:
            serialized message
        """
        data = {**self}
        if 'attachments' in self:
            data['attachments'] = json.dumps(self['attachments'])
        return data

    def to_json(self):
        return json.dumps({**self})


class EventRouter:
    """
    When receiving an event from the RTM API or the slack API it is useful to have a routing mechanisms for
    dispatching event to individual function/coroutine. This class provide such mechanisms for any
    :class:`slack.events.Event`.
    """
    def __init__(self):
        self._routes = defaultdict(dict)

    def register(self, event_type, handler, **detail):
        """
        Register a new handler for a specific :class:`slack.events.Event` `type` (See `slack event types documentation
        <https://api.slack.com/events>`_ for a list of event types).

        The arbitrary keyword argument is used as a key/value pair to compare against what is in the incoming
        :class:`slack.events.Event`

        Args:
            event_type: Event type the handler is interested in
            handler: Callback
            **detail: Additional key for routing
        """
        LOG.info('Registering %s, %s to %s', event_type, detail, handler)
        if len(detail) > 1:
            raise ValueError('Only one detail can be provided for additional routing')
        elif not detail:
            detail_key, detail_value = '*', '*'
        else:
            detail_key, detail_value = detail.popitem()

        if detail_key not in self._routes[event_type]:
            self._routes[event_type][detail_key] = {}

        if detail_value not in self._routes[event_type][detail_key]:
            self._routes[event_type][detail_key][detail_value] = []

        self._routes[event_type][detail_key][detail_value].append(handler)

    def dispatch(self, event):
        """
        Yields handlers matching the routing of the incoming :class:`slack.events.Event`.

        Args:
            event: :class:`slack.events.Event`

        Yields:
            handler
        """
        LOG.debug('Dispatching event "%s"', event.get('type'))
        if event['type'] in self._routes:
            for detail_key, detail_values in self._routes.get(event['type'], {}).items():
                event_value = event.get(detail_key, '*')
                yield from detail_values.get(event_value, [])
        else:
            return


class MessageRouter:
    """
    When receiving an event of type message from the RTM API or the slack API it is useful to have a routing mechanisms
    for dispatching the message to individual function/coroutine. This class provide such mechanisms for any
    :class:`slack.events.Message`.

    The routing is based on regex pattern matching of the message text and the receiving channel.
    """
    def __init__(self):
        self._routes = defaultdict(dict)

    def register(self, pattern, handler, flags=0, channel='*', subtype=None):
        """
        Register a new handler for a specific :class:`slack.events.Message`.

        The routing is based on regex pattern matching the message text and the incoming slack channel.

        Args:
            pattern: Regex pattern matching the message text.
            handler: Callback
            flags: Regex flags.
            channel: Slack channel ID. Use * for any.
            subtype: Message subtype
        """
        LOG.debug('Registering message endpoint "%s: %s"', pattern, handler)
        match = re.compile(pattern, flags)

        if subtype not in self._routes[channel]:
            self._routes[channel][subtype] = dict()

        if match in self._routes[channel][subtype]:
            self._routes[channel][subtype][match].append(handler)
        else:
            self._routes[channel][subtype][match] = [handler]

    def dispatch(self, message):
        """
        Yields handlers matching the routing of the incoming :class:`slack.events.Message`

        Args:
            message: :class:`slack.events.Message`

        Yields:
            handler
        """
        if 'text' in message:
            text = message['text'] or ''
        elif 'message' in message:
            text = message['message'].get('text', '')
        else:
            text = ''

        msg_subtype = message.get('subtype')

        for subtype, matchs in itertools.chain(self._routes[message['channel']].items(), self._routes['*'].items()):
            if msg_subtype == subtype or subtype is None:
                for match, endpoints in matchs.items():
                    if match.search(text):
                        yield from endpoints
