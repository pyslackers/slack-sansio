import pytest
import slack
import slack.actions
import slack.commands
import slack.exceptions


# START: TEST EVENTS
@pytest.mark.parametrize("slack_event", ("channel_deleted", "simple"), indirect=True)
def test_events(slack_event):
    assert slack_event["event"]["type"] in ("channel_deleted", "message")


# END: TEST EVENTS


# START: TEST MESSAGES
@pytest.mark.parametrize(
    "slack_event", {**slack.tests.data.Messages.__members__}, indirect=True
)
def test_messages(slack_event):
    assert slack_event["event"]["type"] == "message"


# END: TEST MESSAGES


# START: TEST ACTIONS
@pytest.mark.parametrize("slack_action", ("button_ok", "button_cancel"), indirect=True)
def test_actions(slack_action):
    action = slack.actions.Action.from_http(slack_action)
    assert action["type"] == "interactive_message"


# END: TEST ACTIONS


# START: TEST COMMANDS
@pytest.mark.parametrize("slack_command", ("text", "no_text"), indirect=True)
def test_commands(slack_command):
    command = slack.commands.Command(slack_command)
    assert command["command"] == "/test"


# END: TEST COMMANDS


# START: TEST CLIENT BODY
@pytest.mark.asyncio
@pytest.mark.parametrize("slack_client", ({"body": "auth_test"},), indirect=True)
async def test_client_body(slack_client):
    data = await slack_client.query(slack.methods.AUTH_TEST)
    assert data["team"] == "TestTeam Workspace"


# END: TEST CLIENT BODY


# START: TEST CLIENT CUSTOM BODY
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "slack_client", ({"body": {"ok": True, "hello": "world"}},), indirect=True
)
async def test_client_custom_body(slack_client):
    data = await slack_client.query(slack.methods.AUTH_TEST)
    assert data == {"ok": True, "hello": "world"}


# END: TEST CLIENT CUSTOM BODY


# START: TEST CLIENT ITER
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "slack_client", ({"body": ["channels_iter", "channels"]},), indirect=True
)
async def test_client_iter(slack_client):
    async for channel in slack_client.iter(slack.methods.CHANNELS_LIST):
        print(channel)


# END: TEST CLIENT ITER

# START: TEST CLIENT STATUS
@pytest.mark.asyncio
@pytest.mark.parametrize("slack_client", ({"status": [200, 500]},), indirect=True)
async def test_client_status(slack_client):

    await slack_client.query(slack.methods.AUTH_TEST)

    with pytest.raises(slack.exceptions.HTTPException):
        await slack_client.query(slack.methods.AUTH_TEST)


# END: TEST CLIENT STATUS


# START: TEST CLIENT MULTIPLE RUN
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "slack_client,ok",
    (({"status": 200}, True), ({"status": 500}, False)),
    indirect=["slack_client"],
)
async def test_client_multiple_run(slack_client, ok):

    if ok:
        await slack_client.query(slack.methods.AUTH_TEST)
    else:
        with pytest.raises(slack.exceptions.HTTPException):
            await slack_client.query(slack.methods.AUTH_TEST)


# END: TEST CLIENT MULTIPLE RUN
