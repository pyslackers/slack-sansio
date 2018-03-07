"""
Collection of functions for sending and decoding request to or from the slack API
"""

import cgi
import json
import logging

from . import exceptions, events, methods, ROOT_URL, HOOK_URL

LOG = logging.getLogger(__name__)

RECONNECT_EVENTS = ('team_migration_started', 'goodbye')
"""Events type preceding a disconnection"""

SKIP_EVENTS = ('reconnect_url', )
"""Events that do not need to be dispatched"""

ITERMODE = ('cursor', 'page', 'timeline')
"""Supported pagination mode"""


def raise_for_status(status, headers, data):
    """
    Check request response status

    Args:
        status: Response status
        headers: Response headers
        data: Response data

    Raises:
        :class:`slack.exceptions.RateLimited`: For 429 status code
        :class:`slack.exceptions:HTTPException`:
    """
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
    """
    Check request response for Slack API error

    Args:
        headers: Response headers
        data: Response data

    Raises:
        :class:`slack.exceptions.SlackAPIError`
    """
    if not data['ok']:
        raise exceptions.SlackAPIError(data.get('error', 'unknow_error'), headers, data)

    if 'warning' in data:
        LOG.warning('Slack API WARNING: %s', data['warning'])


def decode_body(headers, body):
    """
    Decode the response body

    For 'application/json' content-type load the body as a dictionary

    Args:
        headers: Response headers
        body: Response body

    Returns:
        decoded body
    """

    type_, encoding = parse_content_type(headers)
    decoded_body = body.decode(encoding)

    if type_ == 'application/json':
        return json.loads(decoded_body)
    else:
        return decoded_body


def parse_content_type(headers):
    """
    Find content-type and encoding of the response

    Args:
        headers: Response headers

    Returns:
        :py:class:`tuple` (content-type, encoding)
    """
    content_type = headers.get('content-type')
    if not content_type:
        return None, 'utf-8'
    else:
        type_, parameters = cgi.parse_header(content_type)
        encoding = parameters.get("charset", "utf-8")
        return type_, encoding


def prepare_request(url, data, headers, global_headers, token, as_json=None):
    """
    Prepare outgoing request

    Create url, headers, add token to the body if needed json encode it

    Args:
        url: :class:`slack.methods` item or string of url
        data: Outgoing data
        headers: Custom headers
        global_headers: Global headers
        token: Slack API token
        as_json: Post JSON to the slack API
    Returns:
        :py:class:`tuple` (url, body, headers)
    """

    if isinstance(url, methods):
        as_json = as_json or url.value[3]
        url = url.value[0]
    else:
        as_json = False

    if not headers:
        headers = {**global_headers}
    else:
        headers = {**global_headers, **headers}

    if url.startswith(HOOK_URL):
        data, headers = _prepare_json_request(data, token, headers)
    elif url.startswith(ROOT_URL) and not as_json:
        data = _prepare_form_encoded_request(data, token)
    elif url.startswith(ROOT_URL) and as_json:
        data, headers = _prepare_json_request(data, token, headers)
    else:
        url = ROOT_URL + url
        data = _prepare_form_encoded_request(data, token)

    return url, data, headers


def _prepare_json_request(data, token, headers):
    headers['Authorization'] = f'Bearer {token}'
    headers['Content-type'] = 'application/json; charset=utf-8'

    if isinstance(data, events.Message):
        data = data.to_json()
    else:
        data = json.dumps(data or {})

    return data, headers


def _prepare_form_encoded_request(data, token):
    if isinstance(data, events.Message):
        data = data.serialize()

    if not data:
        data = {'token': token}
    elif 'token' not in data:
        data['token'] = token

    return data


def decode_response(status, headers, body):
    """
    Decode incoming response

    Args:
        status: Response status
        headers: Response headers
        body: Response body

    Returns:
        Response data
    """
    data = decode_body(headers, body)
    raise_for_status(status, headers, data)
    raise_for_api_error(headers, data)

    return data


def find_iteration(url, itermode=None, iterkey=None):
    """
    Find iteration mode and iteration key for a given :class:`slack.methods`

    Args:
        url: :class:`slack.methods` or string url
        itermode: Custom iteration mode
        iterkey: Custom iteration key

    Returns:
        :py:class:`tuple` (itermode, iterkey)
    """
    if isinstance(url, methods):
        if not itermode:
            itermode = url.value[1]
        if not iterkey:
            iterkey = url.value[2]

    if not iterkey or not itermode:
        raise ValueError('Iteration not supported for: {}'.format(url))
    elif itermode not in ITERMODE:
        raise ValueError('Iteration not supported for: {}'.format(itermode))

    return itermode, iterkey


def prepare_iter_request(url, data, *, iterkey=None, itermode=None, limit=200, itervalue=None):
    """
    Prepare outgoing iteration request

    Args:
        url: :class:`slack.methods` item or string of url
        data: Outgoing data
        limit: Maximum number of results to return per call.
        iterkey: Key in response data to iterate over (required for url string).
        itermode: Iteration mode (required for url string) (one of `cursor`, `page` or `timeline`)
        itervalue: Value for current iteration (cursor hash, page or timestamp depending on the itermode)
    Returns:
        :py:class:`tuple` (data, iterkey, itermode)
    """
    itermode, iterkey = find_iteration(url, itermode, iterkey)

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

    return data, iterkey, itermode


def decode_iter_request(data):
    """
    Decode incoming response from an iteration request

    Args:
        data: Response data

    Returns:
        Next itervalue
    """
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
    """
    Check if the incoming event needs to be discarded

    Args:
        event: Incoming :class:`slack.events.Event`
        bot_id: Id of connected bot

    Returns:
        boolean
    """
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
    """
    Check if RTM needs reconnecting

    Args:
        event: Incoming :class:`slack.events.Event`

    Returns:
        boolean
    """
    if event['type'] in RECONNECT_EVENTS:
        return True
    else:
        return False
