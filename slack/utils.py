import cgi
import json
import http
import logging

LOG = logging.getLogger(__name__)
ROOT_URL = 'https://slack.com/api/'


class HTTPException(BaseException):
    def __init__(self, status, data):
        self.status = http.HTTPStatus(status)
        self.data = data

    def __str__(self):
        return '{}, {}'.format(self.status.value, self.status.phrase)


class SlackAPIError(BaseException):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return str(self.error)


def raise_for_status(status, data):
    if status != 200:
        raise HTTPException(status, data)


def raise_for_api_error(data):
    if not data['ok']:
        raise SlackAPIError(data.get('error', 'unknow_error'))

    if 'warning' in data:
        LOG.warning(data['warning'])


def decode_body(headers, body):

    type_, encoding = parse_content_type(headers)
    decoded_body = body.decode(encoding)

    if type_ == 'application/json':
        return json.loads(decoded_body)
    else:
        return decoded_body


def parse_content_type(headers):
    content_type = headers.get('content-type')
    if not content_type:
        return None, 'utf-8'
    else:
        type_, parameters = cgi.parse_header(content_type)
        encoding = parameters.get("charset", "utf-8")
        return type_, encoding


def parse_from_rtm(data):
    return json.loads(data)
