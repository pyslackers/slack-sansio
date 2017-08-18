import json
import logging

from collections import defaultdict, MutableMapping
from . import exceptions

LOG = logging.getLogger(__name__)


class Event(MutableMapping):

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
        return self.__class__(self.event, self.metadata)

    @classmethod
    def from_rtm(cls, raw_event):
        if raw_event['type'].startswith('message'):
            return Message(raw_event)
        else:
            return Event(raw_event)

    @classmethod
    def from_http(cls, raw_body, verification_token=None, team_id=None):

        if verification_token and raw_body['token'] != verification_token:
            raise exceptions.FailedVerification(raw_body['token'], raw_body['team_id'])

        if team_id and raw_body['team_id'] != team_id:
            raise exceptions.FailedVerification(raw_body['token'], raw_body['team_id'])

        if raw_body['event']['type'].startswith('message'):
            return Message(raw_body['event'], metadata=raw_body)
        else:
            return Event(raw_body['event'], metadata=raw_body)


class Message(Event):

    def __repr__(self):
        return 'Slack Message: ' + str(self.event)

    def response(self, in_thread=None):

        data = {'channel': self['channel']}

        if in_thread:
            if 'message' in self:
                data['thread_ts'] = self['message'].get('thead_ts') or self['message']['ts']
            else:
                data['thread_ts'] = self.get('thread_ts') or self['ts']
        elif in_thread is None:
            if 'message' in self and 'thread_ts' in self['message']:
                data['thread_ts'] = self['message']['thread_ts']
            elif 'thread_ts' in self:
                data['thread_ts'] = self['thread_ts']

        return Message(data)

    def serialize(self):
        data = {**self}
        if 'attachments' in self:
            data['attachments'] = json.dumps(self['attachments'])
        return data


class Router:

    def __init__(self):
        self._routes = defaultdict(dict)

    def register(self, event_type, handler, **detail):
        LOG.info('Registering %s, %s to %s', event_type, detail, handler.__name__)
        if len(detail) > 1:
            raise TypeError('Only one detail can be provided for additional routing')
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
        LOG.debug('Dispatching event %s', event.get('type'))
        for detail_key, detail_values in self._routes.get(event.get('type')):
            event_value = event.get(detail_key, '*')
            callbacks = detail_values.get(event_value, [])
            for callback in callbacks:
                yield callback
