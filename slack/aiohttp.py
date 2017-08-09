from . import abc


class SlackAPI(abc.SlackAPI):

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = session

    async def _request(self, method, url, headers, body):
        async with self._session.request(method, url, headers=headers,
                                         data=body) as response:
            return response.status, response.headers, await response.read()

    async def post(self, url, data=None):
        data = data or {}
        url, headers, body, *_ = self._pre_request(url, data)
        status, headers, body = await self._request('POST', url, headers, body)
        data, *_ = self._post_request(status, headers, body)
        return data

    async def postiter(self, url, data=None, limit=10, iterkey=None,
                       cursor=None):

        url, headers, body, iterkey = self._pre_request(url, data, limit, cursor, iterkey)
        status, headers, body = await self._request('POST', url, headers, body)
        response_data, cursor = self._post_request(status, headers, body)

        for item in response_data[iterkey]:
            yield item

        if cursor:
            async for item in self.postiter(url, data, limit, iterkey, cursor):
                yield item
