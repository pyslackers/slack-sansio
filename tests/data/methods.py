CHANNELS = {
    "ok": True,
    "channels": [
        {
            "id": "C00000001",
            "name": "fun",
            "created": 1360782804,
            "creator": "U024BE7LH",
            "is_archived": False,
            "is_member": False,
            "num_members": 6,
            "topic": {
                "value": "Fun times",
                "creator": "U024BE7LV",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for fun",
                "creator": "U024BE7LH",
                "last_set": 1360782804
            }
        },
        {
            "id": "C00000002",
            "name": "fun",
            "created": 1360782804,
            "creator": "U024BE7LH",
            "is_archived": False,
            "is_member": False,
            "num_members": 6,
            "topic": {
                "value": "Fun times",
                "creator": "U024BE7LV",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for fun",
                "creator": "U024BE7LH",
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

payloads = {
    'channels_iter': CHANNELS_ITER,
    'channels': CHANNELS
}
