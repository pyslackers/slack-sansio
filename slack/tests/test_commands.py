import pytest
import slack
from slack.commands import Command


class TestCommand:
    def test_fixture(self, command):
        com = Command(command)
        assert isinstance(com, slack.commands.Command)

    def test_parsing_token(self, command):
        slack.commands.Command(command, verification_token="supersecuretoken")

    def test_parsing_team_id(self, command):
        slack.commands.Command(command, team_id="T000AAA0A")

    def test_parsing_wrong_token(self, command):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.commands.Command(command, verification_token="xxx")

    def test_parsing_wrong_team_id(self, command):
        with pytest.raises(slack.exceptions.FailedVerification):
            slack.commands.Command(command, team_id="xxx")

    def test_mapping_access(self, command):
        com = Command(command)
        assert com["user_id"] == "U000AA000"

    def test_mapping_delete(self, command):
        com = Command(command)
        assert com["user_id"] == "U000AA000"
        del com["user_id"]
        with pytest.raises(KeyError):
            print(com["user_id"])

    def test_mapping_set(self, command):
        com = Command(command)
        assert com["user_id"] == "U000AA000"
        com["user_id"] = "foo"
        assert com["user_id"] == "foo"


class TestCommandRouter:
    def test_register(self, command_router):
        def handler():
            pass

        command_router.register("/test", handler)
        assert len(command_router._routes["/test"]) == 1
        assert command_router._routes["/test"][0] is handler

    def test_register_no_slash(self, command_router):
        def handler():
            pass

        command_router.register("test", handler)
        assert len(command_router._routes["/test"]) == 1
        assert command_router._routes["/test"][0] is handler

    def test_multiple_register(self, command_router):
        def handler():
            pass

        def handler_bis():
            pass

        command_router.register("/test", handler)
        command_router.register("/test", handler_bis)
        assert len(command_router._routes["/test"]) == 2
        assert command_router._routes["/test"][0] is handler
        assert command_router._routes["/test"][1] is handler_bis

    def test_dispath(self, command, command_router):
        def handler():
            pass

        handlers = list()
        command_router.register("/test", handler)

        for h in command_router.dispatch(command):
            handlers.append(h)
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_no_dispatch(self, command, command_router):
        def handler():
            pass

        command_router.register("/xxx", handler)
        for h in command_router.dispatch(command):
            assert False

    def test_multiple_dispatch(self, command, command_router):
        def handler():
            pass

        def handler_bis():
            pass

        handlers = list()
        command_router.register("/test", handler)
        command_router.register("/test", handler_bis)

        for h in command_router.dispatch(command):
            handlers.append(h)

        assert len(handlers) == 2
        assert handlers[0] is handler
        assert handlers[1] is handler_bis
