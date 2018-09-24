"""
Collection of functions for sending and decoding request to or from the slack API
"""

import cgi
import hmac
import json
import time
import base64
import hashlib
import logging
from typing import Tuple, Union, Optional, MutableMapping

from . import HOOK_URL, ROOT_URL, events, methods, exceptions

LOG = logging.getLogger(__name__)

RECONNECT_EVENTS = ("team_migration_started", "goodbye")
"""Events type preceding a disconnection"""

SKIP_EVENTS = ("reconnect_url",)
"""Events that do not need to be dispatched"""

ITERMODE = ("cursor", "page", "timeline")
"""Supported pagination mode"""


def raise_for_status(
    status: int, headers: MutableMapping, data: MutableMapping
) -> None:
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

            if isinstance(data, str):
                error = data
            else:
                error = data.get("error", "ratelimited")

            try:
                retry_after = int(headers.get("Retry-After", 1))
            except ValueError:
                retry_after = 1
            raise exceptions.RateLimited(retry_after, error, status, headers, data)
        else:
            raise exceptions.HTTPException(status, headers, data)


def raise_for_api_error(headers: MutableMapping, data: MutableMapping) -> None:
    """
    Check request response for Slack API error

    Args:
        headers: Response headers
        data: Response data

    Raises:
        :class:`slack.exceptions.SlackAPIError`
    """

    if not data["ok"]:
        raise exceptions.SlackAPIError(data.get("error", "unknow_error"), headers, data)

    if "warning" in data:
        LOG.warning("Slack API WARNING: %s", data["warning"])


def decode_body(headers: MutableMapping, body: bytes) -> dict:
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

    # There is one api that just returns `ok` instead of json. In order to have a consistent API we decided to modify the returned payload into a dict.
    if type_ == "application/json":
        payload = json.loads(decoded_body)
    else:
        if decoded_body == "ok":
            payload = {"ok": True}
        else:
            payload = {"ok": False, "data": decoded_body}

    return payload


def parse_content_type(headers: MutableMapping) -> Tuple[Optional[str], str]:
    """
    Find content-type and encoding of the response

    Args:
        headers: Response headers

    Returns:
        :py:class:`tuple` (content-type, encoding)
    """
    content_type = headers.get("content-type")
    if not content_type:
        return None, "utf-8"
    else:
        type_, parameters = cgi.parse_header(content_type)
        encoding = parameters.get("charset", "utf-8")
        return type_, encoding


def prepare_request(
    url: Union[str, methods],
    data: Optional[MutableMapping],
    headers: Optional[MutableMapping],
    global_headers: MutableMapping,
    token: str,
    as_json: Optional[bool] = None,
) -> Tuple[str, Union[str, MutableMapping], MutableMapping]:
    """
    Prepare outgoing request

    Create url, headers, add token to the body and if needed json encode it

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
        real_url = url.value[0]
    else:
        real_url = url
        as_json = False

    if not headers:
        headers = {**global_headers}
    else:
        headers = {**global_headers, **headers}

    payload: Optional[Union[str, MutableMapping]] = None
    if real_url.startswith(HOOK_URL) or (real_url.startswith(ROOT_URL) and as_json):
        payload, headers = _prepare_json_request(data, token, headers)
    elif real_url.startswith(ROOT_URL) and not as_json:
        payload = _prepare_form_encoded_request(data, token)
    else:
        real_url = ROOT_URL + real_url
        payload = _prepare_form_encoded_request(data, token)

    return real_url, payload, headers


def _prepare_json_request(
    data: Optional[MutableMapping], token: str, headers: MutableMapping
) -> Tuple[str, MutableMapping]:
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-type"] = "application/json; charset=utf-8"

    if isinstance(data, events.Message):
        payload = data.to_json()
    else:
        payload = json.dumps(data or {})

    return payload, headers


def _prepare_form_encoded_request(
    data: Optional[MutableMapping], token: str
) -> MutableMapping:
    if isinstance(data, events.Message):
        data = data.serialize()

    if not data:
        data = {"token": token}
    elif "token" not in data:
        data["token"] = token

    return data


def decode_response(status: int, headers: MutableMapping, body: bytes) -> dict:
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


def find_iteration(
    url: Union[methods, str],
    itermode: Optional[str] = None,
    iterkey: Optional[str] = None,
) -> Tuple[str, str]:
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
        raise ValueError("Iteration not supported for: {}".format(url))
    elif itermode not in ITERMODE:
        raise ValueError("Iteration not supported for: {}".format(itermode))

    return itermode, iterkey


def prepare_iter_request(
    url: Union[methods, str],
    data: MutableMapping,
    *,
    iterkey: Optional[str] = None,
    itermode: Optional[str] = None,
    limit: int = 200,
    itervalue: Optional[Union[str, int]] = None,
) -> Tuple[MutableMapping, str, str]:
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

    if itermode == "cursor":
        data["limit"] = limit
        if itervalue:
            data["cursor"] = itervalue
    elif itermode == "page":
        data["count"] = limit
        if itervalue:
            data["page"] = itervalue
    elif itermode == "timeline":
        data["count"] = limit
        if itervalue:
            data["latest"] = itervalue

    return data, iterkey, itermode


def decode_iter_request(data: dict) -> Optional[Union[str, int]]:
    """
    Decode incoming response from an iteration request

    Args:
        data: Response data

    Returns:
        Next itervalue
    """
    if "response_metadata" in data:
        return data["response_metadata"].get("next_cursor")
    elif "paging" in data:
        current_page = int(data["paging"].get("page", 1))
        max_page = int(data["paging"].get("pages", 1))

        if current_page < max_page:
            return current_page + 1
    elif "has_more" in data and data["has_more"] and "latest" in data:
        return data["messages"][-1]["ts"]

    return None


def discard_event(event: events.Event, bot_id: str = None) -> bool:
    """
    Check if the incoming event needs to be discarded

    Args:
        event: Incoming :class:`slack.events.Event`
        bot_id: Id of connected bot

    Returns:
        boolean
    """
    if event["type"] in SKIP_EVENTS:
        return True
    elif bot_id and isinstance(event, events.Message):
        if event.get("bot_id") == bot_id:
            LOG.debug("Ignoring event: %s", event)
            return True
        elif "message" in event and event["message"].get("bot_id") == bot_id:
            LOG.debug("Ignoring event: %s", event)
            return True
    return False


def need_reconnect(event: events.Event) -> bool:
    """
    Check if RTM needs reconnecting

    Args:
        event: Incoming :class:`slack.events.Event`

    Returns:
        boolean
    """
    if event["type"] in RECONNECT_EVENTS:
        return True
    else:
        return False


def validate_request_signature(
    body: str, headers: MutableMapping, signing_secret: str
) -> None:
    """
    Validate incoming request signature using the application signing secret.

    Contrary to the ``team_id`` and ``verification_token`` verification this method is not called by ``slack-sansio`` when creating object from incoming HTTP request. Because the body of the request needs to be provided as text and not decoded as json beforehand.

    Args:
        body: Raw request body
        headers: Request headers
        signing_secret: Application signing_secret

    Raise:
        :class:`slack.exceptions.InvalidSlackSignature`: when provided and calculated signature do not match
        :class:`slack.exceptions.InvalidTimestamp`: when incoming request timestamp is more than 5 minutes old
    """

    request_timestamp = int(headers["X-Slack-Request-Timestamp"])

    if (int(time.time()) - request_timestamp) > (60 * 5):
        raise exceptions.InvalidTimestamp(timestamp=request_timestamp)

    slack_signature = headers["X-Slack-Signature"]
    calculated_signature = (
        "v0="
        + hmac.new(
            signing_secret.encode("utf-8"),
            f"""v0:{headers["X-Slack-Request-Timestamp"]}:{body}""".encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
    )

    if not hmac.compare_digest(slack_signature, calculated_signature):
        raise exceptions.InvalidSlackSignature(slack_signature, calculated_signature)
