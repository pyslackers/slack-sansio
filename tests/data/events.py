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

events = {
    'channel_deleted': CHANNEL_DELETED,
    'pin_added': PIN_ADDED,
    'reaction_added': REACTION_ADDED
}

message = {
    'simple': MESSAGE_SIMPLE,
    'snippet': MESSAGE_SNIPPET,
    'shared': MESSAGE_SHARED,
    'threaded': MESSAGE_THREADED,
    'bot': MESSAGE_BOT,
    'attachment': MESSAGE_ATTACHMENTS,
    'edit': MESSAGE_EDIT,
    'edit_threaded': MESSAGE_EDIT_THREADED,
    'bot_edit': MESSAGE_BOT_EDIT
}
