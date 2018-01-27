import re
import slack
import pytest

from . import data


class TestEvents:
    def test_clone_event(self, event):
        clone = event.clone()
        assert clone == event

    def test_modify_clone(self, event):
        clone = event.clone()
        clone['text'] = 'aaaaa'
        assert clone != event

    def test_parsing(self, raw_event):
        http_event = slack.events.Event.from_http(raw_event)
        rtm_event = slack.events.Event.from_rtm(raw_event['event'])

        assert isinstance(http_event, slack.events.Event)
        assert isinstance(rtm_event, slack.events.Event)
        assert http_event.event == rtm_event.event == raw_event['event']
        assert rtm_event.metadata is None
        assert http_event.metadata == {
            'token': 'supersecuretoken',
            'team_id': 'T000AAA0A',
            'api_app_id': 'A0AAAAAAA',
            'event': http_event.event,
            'type': 'event_callback',
            'authed_teams': ['T000AAA0A'],
            'event_id': 'AAAAAAA',
            'event_time': 123456789
        }

    def test_parsing_token(self, raw_event):
        slack.events.Event.from_http(raw_event, verification_token='supersecuretoken')

    def test_parsing_team_id(self, raw_event):
        slack.events.Event.from_http(raw_event, team_id='T000AAA0A')

    def test_parsing_wrong_token(self, raw_event):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.events.Event.from_http(raw_event, verification_token='xxx')

    def test_parsing_wrong_team_id(self, raw_event):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.events.Event.from_http(raw_event, team_id='xxx')

    @pytest.mark.parametrize('event', ['pin_added', 'reaction_added', 'simple', 'snippet', 'shared', 'threaded', 'bot',
                                       'attachment'],
                             indirect=True)
    def test_mapping_access(self, event):
        assert event['user'] == 'U000AA000'

    @pytest.mark.parametrize('event', ['pin_added', 'reaction_added', 'simple', 'snippet', 'shared', 'threaded', 'bot',
                                       'attachment'],
                             indirect=True)
    def test_mapping_delete(self, event):
        assert event['user'] == 'U000AA000'
        del event['user']
        with pytest.raises(KeyError):
            print(event['user'])

    @pytest.mark.parametrize('event', ['pin_added', 'reaction_added', 'simple', 'snippet', 'shared', 'threaded', 'bot',
                                       'attachment'],
                             indirect=True)
    def test_mapping_set(self, event):
        assert event['user'] == 'U000AA000'
        event['user'] = 'foo'
        assert event['user'] == 'foo'


class TestMessage:
    @pytest.mark.parametrize('raw_event', {**data.Messages.__members__}, indirect=True)
    def test_parsing(self, raw_event):
        http_event = slack.events.Event.from_http(raw_event)
        rtm_event = slack.events.Event.from_rtm(raw_event['event'])

        assert isinstance(http_event, slack.events.Message)
        assert isinstance(rtm_event, slack.events.Message)
        assert http_event.event == rtm_event.event
        assert rtm_event.metadata is None
        assert http_event.metadata == {
            'token': 'supersecuretoken',
            'team_id': 'T000AAA0A',
            'api_app_id': 'A0AAAAAAA',
            'event': http_event.event,
            'type': 'event_callback',
            'authed_teams': ['T000AAA0A'],
            'event_id': 'AAAAAAA',
            'event_time': 123456789
        }

    def test_serialize(self):
        msg = slack.events.Message()
        msg['channel'] = 'C00000A00'
        msg['text'] = 'Hello world'
        assert msg.serialize() == {'channel': 'C00000A00', 'text': 'Hello world'}

    def test_serialize_attachments(self):
        msg = slack.events.Message()
        msg['channel'] = 'C00000A00'
        msg['text'] = 'Hello world'
        msg['attachments'] = {'hello': 'world'}
        assert msg.serialize() == {'channel': 'C00000A00', 'text': 'Hello world', 'attachments': '{"hello": "world"}'}

    def test_response(self, message):
        rep = message.response()
        assert isinstance(rep, slack.events.Message)
        assert rep['channel'] == 'C00000A00'

    def test_response_not_in_thread(self, message):
        rep = message.response(in_thread=False)
        assert rep == {'channel': 'C00000A00'}

    def test_response_in_thread(self, message):
        rep = message.response(in_thread=True)
        assert rep == {'channel': 'C00000A00', 'thread_ts': '123456789.000001'}

    def test_response_thread_default(self, message):
        rep = message.response()
        if 'thread_ts' in message or 'thread_ts' in message.get('message', {}):
            assert rep == {'channel': 'C00000A00', 'thread_ts': '123456789.000001'}
        else:
            assert rep == {'channel': 'C00000A00'}


class TestEventRouter:
    def test_register(self, event_router):
        def handler():
            pass

        event_router.register('channel_deleted', handler)
        assert len(event_router._routes['channel_deleted']['*']['*']) == 1
        assert event_router._routes['channel_deleted']['*']['*'][0] is handler

    def test_register_details(self, event_router):
        def handler():
            pass

        event_router.register('channel_deleted', handler, hello='world')
        assert len(event_router._routes['channel_deleted']['hello']['world']) == 1
        assert event_router._routes['channel_deleted']['hello']['world'][0] is handler

    def test_register_two_details(self, event_router):
        def handler():
            pass

        with pytest.raises(ValueError):
            event_router.register('channel_deleted', handler, hello='world', foo='bar')

    def test_multiple_register(self, event_router):
        def handler():
            pass

        def handler_bis():
            pass

        event_router.register('channel_deleted', handler)
        event_router.register('channel_deleted', handler_bis)
        assert len(event_router._routes['channel_deleted']['*']['*']) == 2
        assert event_router._routes['channel_deleted']['*']['*'][0] is handler
        assert event_router._routes['channel_deleted']['*']['*'][1] is handler_bis

    @pytest.mark.parametrize('event', {**data.Events.__members__}, indirect=True)
    def test_dispatch(self, event, event_router):
        def handler():
            pass

        handlers = list()
        event_router.register('channel_deleted', handler)
        event_router.register('pin_added', handler)
        event_router.register('reaction_added', handler)
        event_router.register('message', handler)

        for h in event_router.dispatch(event):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    @pytest.mark.parametrize('event', {**data.Events.__members__}, indirect=True)
    def test_no_dispatch(self, event, event_router):
        def handler():
            pass

        event_router.register('xxx', handler)
        for h in event_router.dispatch(event):
            assert False

    @pytest.mark.parametrize('event', {**data.Events.__members__}, indirect=True)
    def test_dispatch_details(self, event, event_router):
        def handler():
            pass

        handlers = list()
        event_router.register('channel_deleted', handler, channel='C00000A00')
        event_router.register('pin_added', handler, channel='C00000A00')
        event_router.register('reaction_added', handler, reaction='sirbot')
        event_router.register('message', handler, text=None)

        for h in event_router.dispatch(event):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    @pytest.mark.parametrize('event', {**data.Events.__members__}, indirect=True)
    def test_multiple_dispatch(self, event, event_router):
        def handler():
            pass

        def handler_bis():
            pass

        handlers = list()
        event_router.register('channel_deleted', handler)
        event_router.register('pin_added', handler)
        event_router.register('reaction_added', handler)
        event_router.register('channel_deleted', handler_bis)
        event_router.register('pin_added', handler_bis)
        event_router.register('reaction_added', handler_bis)
        event_router.register('message', handler)
        event_router.register('message', handler_bis)

        for h in event_router.dispatch(event):
            handlers.append(h)
        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis


class TestMessageRouter:
    def test_register(self, message_router):
        def handler():
            pass

        message_router.register('.*', handler)
        assert len(message_router._routes['*'][None][re.compile('.*')]) == 1
        assert message_router._routes['*'][None][re.compile('.*')][0] is handler

    def test_register_channel(self, message_router):
        def handler():
            pass

        message_router.register('.*', handler, channel='C00000A00')
        assert len(message_router._routes['C00000A00'][None][re.compile('.*')]) == 1
        assert message_router._routes['C00000A00'][None][re.compile('.*')][0] is handler

    def test_register_subtype(self, message_router):
        def handler():
            pass

        message_router.register('.*', handler, subtype='bot_message')
        assert len(message_router._routes['*']['bot_message'][re.compile('.*')]) == 1
        assert message_router._routes['*']['bot_message'][re.compile('.*')][0] is handler

    def test_multiple_register(self, message_router):
        def handler():
            pass

        def handler_bis():
            pass

        message_router.register('.*', handler)
        message_router.register('.*', handler_bis)

        assert len(message_router._routes['*'][None][re.compile('.*')]) == 2
        assert message_router._routes['*'][None][re.compile('.*')][0] is handler
        assert message_router._routes['*'][None][re.compile('.*')][1] is handler_bis

    def test_dispatch(self, message_router, message):
        def handler():
            pass

        message_router.register('.*', handler)
        handlers = list()
        for h in message_router.dispatch(message):
            handlers.append(h)

        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_no_dispatch(self, message_router, message):
        def handler():
            pass

        message_router.register('xxx', handler)
        for h in message_router.dispatch(message):
            assert False

    def test_dispatch_pattern(self, message_router, message):
        def handler():
            pass

        message_router.register('hello', handler)
        handlers = list()
        for h in message_router.dispatch(message):
            handlers.append(h)

        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_multiple_dispatch(self, message_router, message):
        def handler():
            pass

        def handler_bis():
            pass

        message_router.register('.*', handler)
        message_router.register('.*', handler_bis)

        handlers = list()
        for h in message_router.dispatch(message):
            handlers.append(h)

        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis

    def test_multiple_dispatch_pattern(self, message_router, message):
        def handler():
            pass

        def handler_bis():
            pass

        message_router.register('hello', handler)
        message_router.register('hello', handler_bis)

        handlers = list()
        for h in message_router.dispatch(message):
            handlers.append(h)

        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis

    def test_dispatch_channel(self, message_router, message):
        def handler():
            pass

        message_router.register('hello', handler, channel='C00000A00')
        handlers = list()
        for h in message_router.dispatch(message):
            handlers.append(h)

        assert len(handlers) == 1
        assert handlers[0] is handler

    @pytest.mark.parametrize('message', ('channel_topic', ), indirect=True)
    def test_dispatch_subtype(self, message_router, message):
        def handler():
            pass

        message_router.register('.*', handler, subtype='channel_topic')
        handlers = list()
        for h in message_router.dispatch(message):
            handlers.append(h)

        assert len(handlers) == 1
        assert handlers[0] is handler
