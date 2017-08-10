import sys
import pprint

from slack.io.sync import SlackAPI


def api(token):
    client = SlackAPI(token=token)
    data = client.post('auth.test')
    pprint.pprint(data)


def rtm(token):
    client = SlackAPI(token=token)
    for msg in client.rtm():
        pprint.pprint(msg)

if __name__ == '__main__':
    TOKEN = sys.argv[1]

    try:
        # api(TOKEN)
        rtm(TOKEN)
    except KeyboardInterrupt:
        pass
