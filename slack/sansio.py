import cgi
import json
import logging

from . import exceptions, events, methods, ROOT_URL

LOG = logging.getLogger(__name__)
RECONNECT_EVENTS = ('team_migration_started', 'goodbye')
SKIP_EVENTS = ('reconnect_url', )


def raise_for_status(status, headers, data):
    if status != 200:
        if status == 429:
            try:
                retry_after = int(headers.get('Retry-After', 1))
            except ValueError:
                retry_after = 1
            raise exceptions.RateLimited(retry_after, data.get('error', 'ratelimited'), status, headers, data)
        else:
            raise exceptions.HTTPException(status, headers, data)


def raise_for_api_error(headers, data):
    if not data['ok']:
        raise exceptions.SlackAPIError(data.get('error', 'unknow_error'), headers, data)

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


def prepare_request(url, data, headers, global_headers, token):
    """Prepare the request"""

    if isinstance(data, events.Message):
        data = data.serialize()

    if isinstance(url, methods):
        url = url.value[0]
    elif not url.startswith(ROOT_URL):
        url = ROOT_URL + url

    if not headers:
        headers = {**global_headers}
    else:
        headers = {**global_headers, **headers}

    if not data:
        data = {'token': token}
    elif 'token' not in data:
        data['token'] = token

    if url.startswith('https://hooks.slack.com'):
        body = json.dumps(data)
    else:
        body = data

    return url, body, headers


def decode_request(status, headers, body):
    """Handle the request response"""

    data = decode_body(headers, body)
    raise_for_status(status, headers, data)
    raise_for_api_error(headers, data)

    return data


def find_iteration(url, itermode, iterkey):

    if isinstance(url, methods):
        if not itermode:
            itermode = url.value[1]
        if not iterkey:
            iterkey = url.value[2]

    if not iterkey or not itermode:
        raise ValueError('Iteration not supported for: {}'.format(url))

    return itermode, iterkey


def prepare_iter_request(url, data, *, iterkey=None, itermode=None, limit=200, itervalue=None):
    itermode, iterkey = find_iteration(url, itermode, iterkey)

    if not data:
        data = {}

    if itermode == 'cursor':
        data['limit'] = limit
        if itervalue:
            data['cursor'] = itervalue
    elif itermode == 'page':
        data['count'] = limit
        if itervalue:
            data['page'] = itervalue
    elif itermode == 'timeline':
        data['count'] = limit
        if itervalue:
            data['latest'] = itervalue
    else:
        raise NotImplementedError('Unknown itermode: %s', itermode)

    return data, iterkey, itermode


def decode_iter_request(data):

    if 'response_metadata' in data:
        return data['response_metadata'].get('next_cursor')
    elif 'paging' in data:
        current_page = int(data['paging'].get('page', 1))
        max_page = int(data['paging'].get('pages', 1))

        if current_page < max_page:
            return current_page + 1
    elif 'has_more' in data and data['has_more'] and 'latest' in data:
        return data['messages'][-1]['ts']


def discard_event(event, bot_id=None):

    if event['type'] in SKIP_EVENTS:
        return True
    elif bot_id and isinstance(event, events.Message):
        if event.get('bot_id') == bot_id:
            LOG.debug('Ignoring event: %s', event)
            return True
        elif 'message' in event and event['message'].get('bot_id') == bot_id:
            LOG.debug('Ignoring event: %s', event)
            return True

    return False


def need_reconnect(event):

    if event['type'] in RECONNECT_EVENTS:
        return True
    else:
        return False
