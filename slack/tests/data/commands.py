from enum import Enum

no_text = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'team_domain': 'teamdomain',
    'channel_id': 'C00000A00',
    'channel_name': 'general',
    'user_id': 'U000AA000',
    'user_name': 'myuser',
    'command': '/test',
    'text': '',
    'response_url': 'https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh',
    'trigger_id': '000000000.0000000000.e1bb750705a2f472e4476c4228cf4784'
}

text = {
    'token': 'supersecuretoken',
    'team_id': 'T000AAA0A',
    'team_domain': 'teamdomain',
    'channel_id': 'C00000A00',
    'channel_name': 'general',
    'user_id': 'U000AA000',
    'user_name': 'myuser',
    'command': '/test',
    'text': 'foo bar',
    'response_url': 'https://hooks.slack.com/actions/T000AAA0A/123456789123/YTC81HsJRuuGSLVFbSnlkJlh',
    'trigger_id': '000000000.0000000000.e1bb750705a2f472e4476c4228cf4784'
}


class Commands(Enum):
    """
    List of available command for testing

        - text
        - no_text

    """
    text = text
    no_text = no_text
