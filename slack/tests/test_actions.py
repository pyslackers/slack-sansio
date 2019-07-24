import pytest
import slack
from slack.actions import Action, Router

from . import data


class TestActions:
    def test_from_http(self, slack_action):
        act = Action.from_http(slack_action)
        assert isinstance(act, slack.actions.Action)

    def test_parsing_token(self, slack_action):
        slack.actions.Action.from_http(
            slack_action, verification_token="supersecuretoken"
        )

    def test_parsing_team_id(self, slack_action):
        slack.actions.Action.from_http(slack_action, team_id="T000AAA0A")

    def test_parsing_wrong_token(self, slack_action):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.actions.Action.from_http(slack_action, verification_token="xxx")

    def test_parsing_wrong_team_id(self, slack_action):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.actions.Action.from_http(slack_action, team_id="xxx")

    def test_mapping_access(self, slack_action):
        act = Action.from_http(slack_action)
        assert act["callback_id"] == "test_action"

    def test_mapping_delete(self, slack_action):
        act = Action.from_http(slack_action)
        assert act["callback_id"] == "test_action"
        del act["callback_id"]
        with pytest.raises(KeyError):
            print(act["callback_id"])

    def test_mapping_set(self, slack_action):
        act = Action.from_http(slack_action)
        assert act["callback_id"] == "test_action"
        act["callback_id"] = "foo"
        assert act["callback_id"] == "foo"


class TestActionRouter:
    def test_register(self, action_router):
        def handler():
            pass

        action_router.register("test_action", handler)
        assert len(action_router._routes["test_action"]["*"]) == 1
        assert action_router._routes["test_action"]["*"][0] is handler

    def test_register_name(self, action_router):
        def handler():
            pass

        action_router.register("test_action", handler, name="aaa")
        assert len(action_router._routes["test_action"]["aaa"]) == 1
        assert action_router._routes["test_action"]["aaa"][0] is handler

    def test_multiple_register(self, action_router):
        def handler():
            pass

        def handler_bis():
            pass

        action_router.register("test_action", handler)
        action_router.register("test_action", handler_bis)
        assert len(action_router._routes["test_action"]["*"]) == 2
        assert action_router._routes["test_action"]["*"][0] is handler
        assert action_router._routes["test_action"]["*"][1] is handler_bis

    def test_register_block(self, action_router: Router):
        def handler():
            pass

        action_router.register_block_action("test_block_id", handler)

        assert len(action_router._routes["test_block_id"]["*"]) == 1
        assert action_router._routes["test_block_id"]["*"][0] is handler

    def test_register_block_action_id(self, action_router: Router):
        def handler():
            pass

        action_router.register_block_action(
            "test_block_id", handler, action_id="test_action_id"
        )

        assert len(action_router._routes["test_block_id"]["test_action_id"]) == 1
        assert action_router._routes["test_block_id"]["test_action_id"][0] is handler

    def test_multiple_register_block(self, action_router: Router):
        def handler():
            pass

        def handler_bis():
            pass

        action_router.register_block_action("test_block_id", handler)
        action_router.register_block_action("test_block_id", handler_bis)

        assert len(action_router._routes["test_block_id"]["*"]) == 2
        assert action_router._routes["test_block_id"]["*"][0] is handler
        assert action_router._routes["test_block_id"]["*"][1] is handler_bis

    def test_register_dialog_submission(self, action_router: Router):
        def handler():
            pass

        action_router.register_dialog_submission("test_action", handler)

        assert len(action_router._routes["test_action"]["*"]) == 1
        assert action_router._routes["test_action"]["*"][0] is handler

    def test_register_interactive_message(self, action_router: Router):
        def handler():
            pass

        action_router.register_interactive_message("test_action", handler)

        assert len(action_router._routes["test_action"]["*"]) == 1
        assert action_router._routes["test_action"]["*"][0] is handler

    def test_dispath(self, slack_action, action_router):
        def handler():
            pass

        act = Action.from_http(slack_action)
        action_router.register("test_action", handler)

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_no_dispatch(self, slack_action, action_router):
        def handler():
            pass

        act = Action.from_http(slack_action)
        action_router.register("xxx", handler)

        for h in action_router.dispatch(act):
            assert False

    @pytest.fixture(params={**data.InteractiveMessage.__members__})
    def test_dispatch_details(self, slack_action, action_router):
        def handler():
            pass

        act = Action.from_http(slack_action)
        action_router.register("test_action", handler, name="ok")
        action_router.register("test_action", handler, name="cancel")

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_dispatch_action_specific_registration_methods(
        self, slack_action, action_router
    ):
        def handler():
            pass

        act = Action.from_http(slack_action)

        if act["type"] in ("interactive_message", "message_action"):
            action_router.register_interactive_message("test_action", handler)
        elif act["type"] == "dialog_submission":
            action_router.register_dialog_submission("test_action", handler)
        elif act["type"] == "block_actions":
            action_router.register_block_action("test_block_id", handler)

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_dispatch_block_action(self, block_action, action_router):
        def handler():
            pass

        act = Action.from_http(block_action)
        action_router.register_block_action("test_block_id", handler)
        action_router.register("test_other_block_id", handler)

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_dispatch_block_action_with_id(self, block_action, action_router):
        def handler():
            pass

        act = Action.from_http(block_action)
        action_router.register_block_action(
            "test_block_id", handler, action_id="test_action_id"
        )

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_multiple_dispatch(self, slack_action, action_router):
        def handler():
            pass

        def handler_bis():
            pass

        act = Action.from_http(slack_action)
        action_router.register("test_action", handler)
        action_router.register("test_action", handler_bis)

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)

        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis

    def test_multiple_block_dispatch(self, block_action, action_router):
        def handler():
            pass

        def handler_bis():
            pass

        act = Action.from_http(block_action)
        action_router.register_block_action("test_block_id", handler)
        action_router.register_block_action("test_block_id", handler_bis)

        handlers = list()
        for h in action_router.dispatch(act):
            handlers.append(h)

        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis

    def test_dispatch_unhandle_type(self, action_router):

        action = {"type": "unhandled_type", "callback_id": "test_action"}

        with pytest.raises(slack.actions.UnknownActionType):
            for _ in action_router.dispatch(action):
                pass
