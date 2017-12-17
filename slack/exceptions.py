import http


class HTTPException(Exception):
    """
    Raised on non 200 status code

    Attributes:
        headers: Response headers
        data: Response data
        status: Response status
    """
    def __init__(self, status, headers, data):
        self.headers = headers
        self.data = data

        self.status = http.HTTPStatus(status)

    def __str__(self):
        return '{}, {}'.format(self.status.value, self.status.phrase)


class SlackAPIError(Exception):
    """
    Raised for errors return by the Slack API

    Attributes:
        headers: Response headers
        data: Response data
        error: Slack API error
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

    Attributes:
        retry_after: Timestamp when the rate limitation ends
    """
    def __init__(self, retry_after, error, status, headers, data):
        HTTPException.__init__(self, status=status, headers=headers, data=data)
        SlackAPIError.__init__(self, error=error, headers=headers, data=data)
        self.retry_after = retry_after

    def __str__(self):
        return HTTPException.__str__(self) + ', retry in {}s'.format(self.retry_after)


class FailedVerification(Exception):
    """
    Raised when incoming data from Slack webhooks fail verification

    Attributes:
        token: Token that failed verification
        team_id: Team id that failed verification
    """
    def __init__(self, token, team_id):
        self.token = token
        self.team_id = team_id
