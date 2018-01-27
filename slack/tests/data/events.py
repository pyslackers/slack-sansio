import json

from enum import Enum

CHANNEL_DELETED = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'channel_deleted',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

PIN_ADDED = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'pin_added',
        'user': 'U000AA000',
        'channel': 'C00000A00',
        'item': {
            'type': 'message',
            'channel': 'C00000A00',
            'message': {
                'type': 'message',
                'user': 'U000AA000',
                'text': 'hello world',
                'ts': '123456789.000001',
                'permalink': 'https://team.slack.com/archives/C00000A00/p123456789000001',
                'pinned_to': ['C00000A00']
            },
            'created': 1513860592,
            'created_by': 'U000AA000'
        },
        'item_user': 'U000AA000',
        'pin_count': 1,
        'event_ts': '1513860592.000014'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

REACTION_ADDED = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'reaction_added',
        'user': 'U000AA000',
        'item': {
            'type': 'message',
            'channel': 'C00000A00',
            'ts': '123456789.000001'
        },
        'reaction': 'sirbot',
        'item_user': 'U000AA000',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_SIMPLE = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': 'hello world',
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_MENTION = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': '<@U0AAA0A00> hello world',
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_SNIPPET = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': '```\nhello world\n```',
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_SHARED = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': 'hello',
        'attachments': [
            {
                'fallback': '[December 1st, 2000 1:01 PM] ovv: <@U000AA000> hello',
                'ts': '123456789.000001',
                'author_id': 'U000AA000',
                'author_subname': 'Ovv',
                'channel_id': 'C00000A00',
                'channel_name': 'general',
                'is_msg_unfurl': True,
                'text': 'hello',
                'author_name': 'Ovv',
                'author_link': 'https://team.slack.com/team/U000AA000',
                'author_icon': 'https://avatars.slack-edge.com/2000-01-01/111111111_11111111111_48.jpg',
                'mrkdwn_in': ['text'],
                'color': 'D0D0D0',
                'from_url': 'https://team.slack.com/archives/C00000A00/p123456789000001',
                'is_share': True,
                'footer': 'Posted in #hello'
            }
        ],
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_THREADED = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': 'hello world',
        'thread_ts': '123456789.000001',
        'parent_user_id': 'U000AA001',
        'ts': '987654321.000001',
        'channel': 'C00000A00',
        'event_ts': '987654321.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_BOT = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': 'hello world',
        'bot_id': 'B0AAA0A00',
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_ATTACHMENTS = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'user': 'U000AA000',
        'text': 'hello',
        'attachments': [
            {
                'fallback': 'Required plain-text summary of the attachment.',
                'text': 'hello world',
                'id': 1,
                'color': '36a64f'
            }
        ],
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_EDIT = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'message': {
            'type': 'message',
            'user': 'U000AA000',
            'text': 'hello world',
            'edited': {
                'user': 'U000AA000',
                'ts': '1513882449.000000'
            },
            'ts': '123456789.000001'
        },
        'subtype': 'message_changed',
        'hidden': True,
        'channel': 'C00000A00',
        'previous_message': {
            'type': 'message',
            'user': 'U000AA000',
            'text': 'foo bar',
            'ts': '123456789.000001'
        },
        'event_ts': '123456789.000002',
        'ts': '123456789.000002'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_BOT_EDIT = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'message': {
            'type': 'message',
            'user': 'U000AA000',
            'text': 'hello world',
            'bot_id': 'B0AAA0A00',
            'edited': {
                'user': 'U000AA000',
                'ts': '1513882449.000000'
            },
            'ts': '123456789.000001'
        },
        'subtype': 'message_changed',
        'hidden': True,
        'channel': 'C00000A00',
        'previous_message': {
            'type': 'message',
            'user': 'U000AA000',
            'text': 'foo bar',
            'ts': '123456789.000001',
            'bot_id': 'B0AAA0A00'
        },
        'event_ts': '123456789.000002',
        'ts': '123456789.000002'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_EDIT_THREADED = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'type': 'message',
        'message': {
            'type': 'message',
            'user': 'U000AA000',
            'text': 'hello',
            'edited': {
                'user': 'U000AA000',
                'ts': '1513882759.000000'
            },
            'thread_ts': '123456789.000001',
            'parent_user_id': 'U000AA000',
            'ts': '1513882746.000279'
        },
        'subtype': 'message_changed',
        'hidden': True,
        'channel': 'C00000A00',
        'previous_message': {
            'type': 'message',
            'user': 'U000AA000',
            'text': 'foo bar',
            'thread_ts': '123456789.000001',
            'parent_user_id': 'U000AA000',
            'ts': '123456789.000001'
        },
        'event_ts': '123456789.000002',
        'ts': '123456789.000002'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_NONE_TEXT = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'bot_id': 'B092ZCBCY',
        'attachments': [
            {
                'fallback': '''<https://twitter.com/ThePSF|@ThePSF>: JupyterCon 2018: Call For Proposals: '''
                            '''<https://blog.jupyter.org/jupytercon-2018-call-for-proposal-87986014ee0b>. '''
                            '''<https://twitter.com/ProjectJupyter|@ProjectJupyter>''''',
                'ts': 1516989711, 'author_name': 'Python Software',
                'author_link': 'https://twitter.com/ThePSF/status/956950323523932160',
                'author_icon': 'https://pbs.twimg.com/profile_images/439154912719413248/pUBY5pVj_normal.png',
                'author_subname': '@ThePSF',
                'pretext': '<https://twitter.com/ThePSF/status/956950323523932160>',
                'text': '''JupyterCon 2018: Call For Proposals: '''
                        '''<https://blog.jupyter.org/jupytercon-2018-call-for-proposal-87986014ee0b>. '''
                        '''<https://twitter.com/ProjectJupyter|@ProjectJupyter>''',
                'service_name': 'twitter',
                'service_url': 'https://twitter.com/',
                'from_url': 'https://twitter.com/ThePSF/status/956950323523932160',
                'id': 1, 'footer': 'Twitter',
                'footer_icon': 'https://a.slack-edge.com/6e067/img/services/twitter_pixel_snapped_32.png'
            }
        ],
        'text': None,
        'type': 'message',
        'subtype': 'bot_message',
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

MESSAGE_CHANNEL_TOPIC = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'api_app_id': 'A0AAAAAAA',
    'event': {
        'user': 'U299GM524',
        'topic': 'Company-wide announcements and work-based matter hello',
        'text': '<@U299GM524> set the channel topic: Company-wide announcements and work-based matter hello',
        'type': 'message',
        'subtype': 'channel_topic',
        'ts': '123456789.000001',
        'channel': 'C00000A00',
        'event_ts': '123456789.000001'
    },
    'type': 'event_callback',
    'authed_teams': ['T000AAA0A'],
    'event_id': 'AAAAAAA',
    'event_time': 123456789
}

GOODBYE = {
    "type": "goodbye"
}

RECONNECT_URL = {
    "type": "reconnect_url",
    "url": "wss:\/\/testteam.slack.com/012345678910"
}


class Events(Enum):
    """
    List of available event for testing

        - channel_deleted
        - pin_added
        - reaction_added

    """
    channel_deleted = CHANNEL_DELETED
    pin_added = PIN_ADDED
    reaction_added = REACTION_ADDED
    non_text = MESSAGE_NONE_TEXT


class RTMEvents(Enum):
    """
    List of available rtm event for testing

        - channel_deleted
        - pin_added
        - goodbye
        - message_bot
        - reconnect_url

    """
    channel_deleted = json.dumps(CHANNEL_DELETED['event'])
    pin_added = json.dumps(PIN_ADDED['event'])
    goodbye = json.dumps(GOODBYE)
    message_bot = json.dumps(MESSAGE_BOT['event'])
    reconnect_url = json.dumps(RECONNECT_URL)


class Messages(Enum):
    """
    List of available message for testing

        - simple
        - snippet
        - shared
        - threaded
        - bot
        - bot_edit
        - attachment
        - edit
        - edit_threaded
        - mention
        - none_text
        - channel_topic

    """
    simple = MESSAGE_SIMPLE
    snippet = MESSAGE_SNIPPET
    shared = MESSAGE_SHARED
    threaded = MESSAGE_THREADED
    bot = MESSAGE_BOT
    bot_edit = MESSAGE_BOT_EDIT
    attachment = MESSAGE_ATTACHMENTS
    edit = MESSAGE_EDIT
    edit_threaded = MESSAGE_EDIT_THREADED
    mention = MESSAGE_MENTION
    channel_topic = MESSAGE_CHANNEL_TOPIC
