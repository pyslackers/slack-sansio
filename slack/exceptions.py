import http


class HTTPException(BaseException):
    """
    Raised on non 200 status code

    """
    def __init__(self, status, headers, data):
        self.headers = headers
        self.data = data

        self.status = http.HTTPStatus(status)

    def __str__(self):
        return '{}, {}'.format(self.status.value, self.status.phrase)


class SlackAPIError(BaseException):
    """
    Raised for errors return by the Slack API
    """
    def __init__(self, error, headers, data):
        self.headers = headers
        self.data = data

        self.error = error

    def __str__(self):
        return str(self.error)


class RateLimited(HTTPException, SlackAPIError):
    """
    Raised when rate limited when `retry_when_rate_limit` is `False`
    """
    def __init__(self, retry_after, error, status, headers, data):
        HTTPException.__init__(self, status=status, headers=headers, data=data)
        SlackAPIError.__init__(self, error=error, headers=headers, data=data)
        self.retry_after = retry_after

    def __str__(self):
        return HTTPException.__str__(self) + ', retry in {}s'.format(self.retry_after)


class FailedVerification(BaseException):
    """
    Raised when incoming data from Slack webhooks fail verification
    """
    def __init__(self, token, team_id):
        self.token = token
        self.team_id = team_id


class UnknownHandler(BaseException):
    pass


class UnknownAction(UnknownHandler):
    """
    Raised when no route can be found for incoming :class:`slack.actions.Action`
    """
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return 'Unknown callback_id: {}'.format(self.action.get('callback_id'))
