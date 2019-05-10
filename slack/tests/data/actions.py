import json
from enum import Enum

button_ok = {
    "type": "interactive_message",
    "actions": [{"name": "ok", "type": "button", "value": "hello"}],
    "callback_id": "test_action",
    "team": {"id": "T000AAA0A", "domain": "team"},
    "channel": {"id": "C00000A00", "name": "general"},
    "user": {"id": "U000AA000", "name": "username"},
    "action_ts": "987654321.000001",
    "message_ts": "123456789.000001",
    "attachment_id": "1",
    "token": "supersecuretoken",
    "is_app_unfurl": False,
    "response_url": "https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh",
    "trigger_id": "000000000.0000000000.e1bb750705a2f472e4476c4228cf4784",
}

button_cancel = {
    "type": "interactive_message",
    "actions": [{"name": "cancel", "type": "button", "value": "hello"}],
    "callback_id": "test_action",
    "team": {"id": "T000AAA0A", "domain": "team"},
    "channel": {"id": "C00000A00", "name": "general"},
    "user": {"id": "U000AA000", "name": "username"},
    "action_ts": "987654321.000001",
    "message_ts": "123456789.000001",
    "attachment_id": "1",
    "token": "supersecuretoken",
    "is_app_unfurl": False,
    "response_url": "https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh",
    "trigger_id": "000000000.0000000000.e1bb750705a2f472e4476c4228cf4784",
}

dialog_submission = {
    "type": "dialog_submission",
    "submission": {"foo": "bar"},
    "callback_id": "test_action",
    "team": {"id": "T000AAA0A", "domain": "team"},
    "user": {"id": "U000AA000", "name": "username"},
    "channel": {"id": "C00000A00", "name": "general"},
    "action_ts": "987654321.000001",
    "token": "supersecuretoken",
    "response_url": "https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh",
}

message_action = {
    "type": "message_action",
    "token": "supersecuretoken",
    "action_ts": "987654321.000001",
    "team": {"id": "T000AAA0A", "domain": "team"},
    "user": {"id": "U000AA000", "name": "username"},
    "channel": {"id": "C00000A00", "name": "general"},
    "callback_id": "test_action",
    "trigger_id": "418799722116.77329528181.9c7441638716b0b9b698f3d8ae73d9c1",
    "message_ts": "1534605601.000100",
    "message": {
        "type": "message",
        "user": "U000AA000",
        "text": "test message",
        "client_msg_id": "904f281d-338e-4621-a56f-afbfc80b3c59",
        "ts": "1534605601.000100",
    },
    "response_url": "https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh",
}

block_action = {
    "type": "block_actions",
    "token": "supersecuretoken",
    "action_ts": "987654321.000001",
    "team": {"id": "T000AAA0A", "domain": "team"},
    "user": {"id": "U000AA000", "name": "username"},
    "channel": {"id": "C00000A00", "name": "general"},
    "trigger_id": "418799722116.77329528181.9c7441638716b0b9b698f3d8ae73d9c1",
    "message_ts": "1534605601.000100",
    "message": {
        "type": "message",
        "user": "U000AA000",
        "text": "test message",
        "client_msg_id": "904f281d-338e-4621-a56f-afbfc80b3c59",
        "ts": "1534605601.000100",
    },
    "actions": [
        {
            "type": "static_select",
            "block_id": "test_block_id",
            "action_id": "test_action_id",
            "selected_option": {
                "text": {"type": "plain_text", "text": "Edit it"},
                "value": "value-0",
            },
            "placeholder": {"type": "plain_text", "text": "Manage"},
            "action_ts": "1557505776.632169",
        }
    ],
    "response_url": "https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh",
}

raw_button_ok = {"payload": json.dumps(button_ok)}
raw_button_cancel = {"payload": json.dumps(button_cancel)}
raw_dialog_submission = {"payload": json.dumps(dialog_submission)}
raw_message_action = {"payload": json.dumps(message_action)}
raw_block_action = {"payload": json.dumps(block_action)}


class InteractiveMessage(Enum):
    """
    List of available interactive message action for testing

        - button_ok
        - button_cancel

    """

    button_ok = raw_button_ok
    button_cancel = raw_button_cancel


class DialogSubmission(Enum):
    """
    List of available dialog submission action for testing

        - dialog_submission

    """

    dialog_submission = raw_dialog_submission


class MessageAction(Enum):
    """
    List of available message action submission for testing

        - action
    """

    action = raw_message_action


class BlockAction(Enum):
    """
    List of available block action for testing

        - option_select
    """

    option_select = raw_block_action
