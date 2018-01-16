from enum import Enum

CHANNELS = {
    "ok": True,
    "channels": [
        {
            "id": "C00000001",
            "name": "fun",
            "created": 1360782804,
            "creator": "U000AA000",
            "is_archived": False,
            "is_member": False,
            "num_members": 6,
            "topic": {
                "value": "Fun times",
                "creator": "U000AA000",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for fun",
                "creator": "U000AA000",
                "last_set": 1360782804
            }
        },
        {
            "id": "C00000002",
            "name": "fun",
            "created": 1360782804,
            "creator": "U000AA000",
            "is_archived": False,
            "is_member": False,
            "num_members": 6,
            "topic": {
                "value": "Fun times",
                "creator": "U000AA000",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for fun",
                "creator": "U000AA000",
                "last_set": 1360782804
            }
        }
    ]
}


CHANNELS_ITER = {
    "ok": True,
    "channels": CHANNELS['channels'],
    "response_metadata": {
        "next_cursor": "wxyz"
    }
}

USERS_INFO = {
    "ok": True,
    "user": {
        "id": "W012A3CDE",
        "team_id": "T012AB3C4",
        "name": "sirbotalotr",
        "deleted": True,
        "color": "9f69e7",
        "real_name": "episod",
        "tz": "America\/Los_Angeles",
        "tz_label": "Pacific Daylight Time",
        "tz_offset": -25200,
        "profile": {
            "avatar_hash": "ge3b51ca72de",
            "status_text": "Print is dead",
            "status_emoji": ":books:",
            "real_name": "Egon Spengler",
            "display_name": "spengler",
            "real_name_normalized": "Egon Spengler",
            "display_name_normalized": "spengler",
            "email": "spengler@ghostbusters.example.com",
            "image_24": "https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_32": "https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_48": "https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_72": "https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_192": "https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_512": "https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "team": "T012AB3C4",
            "bot_id": "B0AAA0A00"
        },
        "is_admin": True,
        "is_owner": False,
        "is_primary_owner": False,
        "is_restricted": False,
        "is_ultra_restricted": False,
        "is_bot": True,
        "updated": 1502138686,
        "is_app_user": False,
        "has_2fa": False
    }
}

AUTH_TEST = {
    "ok": True,
    "url": "https:\/\/testteam.slack.com\/",
    "team": "TestTeam Workspace",
    "user": "sirbotalot",
    "team_id": "T12345678",
    "user_id": "W12345678"
}

RTM_CONNECT = {
    "ok": True,
    "self": {
        "id": "W012A3CDE",
        "name": "sirbotalot"
    },
    "team": {
        "domain": "testteam",
        "id": "T12345678",
        "name": "testteam"
    },
    "url": "wss:\/\/testteam.slack.com/012345678910"
}


class Methods(Enum):
    """
    List of available methods for testing

        - channels
        - channels_iter (channels with a cursor)
        - users_info
        - auth_test
        - rtm_connect

    """
    channels_iter = CHANNELS_ITER
    channels = CHANNELS
    users_info = USERS_INFO
    auth_test = AUTH_TEST
    rtm_connect = RTM_CONNECT
