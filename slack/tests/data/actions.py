import json

from enum import Enum

button_ok = {
    'type': 'interactive_message',
    'actions': [
        {
            'name': 'ok',
            'type': 'button',
            'value': 'hello'
        }
    ],
    'callback_id': 'test_action',
    'team': {
        'id': 'T000AAA0A',
        'domain': 'team'
    },
    'channel': {
        'id': 'C00000A00',
        'name': 'general'
    },
    'user': {
        'id': 'U000AA000',
        'name': 'username'
    },
    'action_ts': '987654321.000001',
    'message_ts': '123456789.000001',
    'attachment_id': '1',
    'token': 'supersecuretoken',
    'is_app_unfurl': False,
    'response_url': 'https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh',
    'trigger_id': '000000000.0000000000.e1bb750705a2f472e4476c4228cf4784'
}

button_cancel = {
    'type': 'interactive_message',
    'actions': [
        {
            'name': 'cancel',
            'type': 'button',
            'value': 'hello'
        }
    ],
    'callback_id': 'test_action',
    'team': {
        'id': 'T000AAA0A',
        'domain': 'team'
    },
    'channel': {
        'id': 'C00000A00',
        'name': 'general'
    },
    'user': {
        'id': 'U000AA000',
        'name': 'username'
    },
    'action_ts': '987654321.000001',
    'message_ts': '123456789.000001',
    'attachment_id': '1',
    'token': 'supersecuretoken',
    'is_app_unfurl': False,
    'response_url': 'https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh',
    'trigger_id': '000000000.0000000000.e1bb750705a2f472e4476c4228cf4784'
}

dialog_submission = {
    'type': 'dialog_submission',
    'submission': {
        'foo': 'bar'
    },
    'callback_id': 'test_action',
    'team': {
        'id': 'T000AAA0A',
        'domain': 'team'
    },
    'user': {
        'id': 'U000AA000',
        'name': 'username'
    },
    'channel': {
        'id': 'C00000A00',
        'name': 'general'
    },
    'action_ts': '987654321.000001',
    'token': 'supersecuretoken',
    'response_url': 'https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh'
}

raw_button_ok = {'payload': json.dumps(button_ok)}
raw_button_cancel = {'payload': json.dumps(button_cancel)}
raw_dialog_submission = {'payload': json.dumps(dialog_submission)}


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
