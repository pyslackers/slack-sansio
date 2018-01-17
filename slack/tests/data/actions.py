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

raw_button_ok = {'payload': json.dumps(button_ok)}
raw_button_cancel = {'payload': json.dumps(button_cancel)}


class Actions(Enum):
    """
    List of available action for testing

        - button_ok
        - button_cancel

    """
    button_ok = raw_button_ok
    button_cancel = raw_button_cancel
