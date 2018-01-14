import slack
import pytest


class TestActions:
    def test_from_http(self, action):
        assert isinstance(action, slack.actions.Action)

    def test_parsing_token(self, raw_action):
        slack.actions.Action.from_http(raw_action, verification_token='supersecuretoken')

    def test_parsing_team_id(self, raw_action):
        slack.actions.Action.from_http(raw_action, team_id='T000AAA0A')

    def test_parsing_wrong_token(self, raw_action):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.actions.Action.from_http(raw_action, verification_token='xxx')

    def test_parsing_wrong_team_id(self, raw_action):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.actions.Action.from_http(raw_action, team_id='xxx')

    def test_mapping_access(self, action):
        assert action['callback_id'] == 'test_action'

    def test_mapping_delete(self, action):
        assert action['callback_id'] == 'test_action'
        del action['callback_id']
        with pytest.raises(KeyError):
            print(action['callback_id'])

    def test_mapping_set(self, action):
        assert action['callback_id'] == 'test_action'
        action['callback_id'] = 'foo'
        assert action['callback_id'] == 'foo'


class TestActionRouter:
    def test_register(self, action_router):
        def handler():
            pass

        action_router.register('test_action', handler)
        assert len(action_router._routes['test_action']['*']) == 1
        assert action_router._routes['test_action']['*'][0] is handler

    def test_register_name(self, action_router):
        def handler():
            pass

        action_router.register('test_action', handler, name='aaa')
        assert len(action_router._routes['test_action']['aaa']) == 1
        assert action_router._routes['test_action']['aaa'][0] is handler

    def test_multiple_register(self, action_router):
        def handler():
            pass

        def handler_bis():
            pass

        action_router.register('test_action', handler)
        action_router.register('test_action', handler_bis)
        assert len(action_router._routes['test_action']['*']) == 2
        assert action_router._routes['test_action']['*'][0] is handler
        assert action_router._routes['test_action']['*'][1] is handler_bis

    def test_dispath(self, action, action_router):
        def handler():
            pass

        handlers = list()
        action_router.register('test_action', handler)

        for h in action_router.dispatch(action):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_no_dispatch(self, action, action_router):
        def handler():
            pass

        action_router.register('xxx', handler)
        for h in action_router.dispatch(action):
            assert False

    def test_dispatch_details(self, action, action_router):
        def handler():
            pass

        handlers = list()
        action_router.register('test_action', handler, name='ok')
        action_router.register('test_action', handler, name='cancel')

        for h in action_router.dispatch(action):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_multiple_dispatch(self, action, action_router):
        def handler():
            pass

        def handler_bis():
            pass

        handlers = list()
        action_router.register('test_action', handler)
        action_router.register('test_action', handler_bis)

        for h in action_router.dispatch(action):
            handlers.append(h)

        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis
