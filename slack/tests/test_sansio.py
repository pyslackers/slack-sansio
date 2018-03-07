import time
import json
import pytest
import logging

from slack import sansio, exceptions, methods


class TestRequest:
    def test_prepare_request(self, token):
        url, body, headers = sansio.prepare_request(methods.AUTH_TEST, {}, {}, {}, token)
        assert url == 'https://slack.com/api/auth.test'
        assert body == '{}'
        assert 'Authorization' in headers
        assert 'Content-type' in headers
        assert headers['Content-type'] == 'application/json; charset=utf-8'

        url, body, headers = sansio.prepare_request(methods.AUTH_REVOKE, {}, {}, {}, token)
        assert url == 'https://slack.com/api/auth.revoke'
        assert body == {'token': token}
        assert headers == {}

    @pytest.mark.parametrize('url', (methods.AUTH_TEST, 'auth.test', 'https://slack.com/api/auth.test'))
    def test_prepare_request_urls(self, url):
        clean_url, _, _ = sansio.prepare_request(url, {}, {}, {}, '')
        assert clean_url == 'https://slack.com/api/auth.test'

    def test_prepare_request_url_hook(self):
        clean_url, _, _ = sansio.prepare_request('https://hooks.slack.com/T0000000/aczvrfver', {}, {}, {}, '')
        assert clean_url == 'https://hooks.slack.com/T0000000/aczvrfver'

    @pytest.mark.parametrize('payload,result', (
        ({'foo': 'bar'}, {'foo': 'bar'}),
        (
            {'foo': 'bar', 'attachements': [{'a': 'b'}]},
            {'foo': 'bar', 'attachements': [{'a': 'b'}]}
        ),
    ))
    def test_prepare_request_body(self, token, payload, result):
        _, body, headers = sansio.prepare_request(methods.AUTH_TEST, payload, {}, {}, token)

        assert isinstance(body, str)
        assert body == json.dumps(result)
        assert 'Authorization' in headers
        assert 'Content-type' in headers
        assert headers['Content-type'] == 'application/json; charset=utf-8'

        _, body, headers = sansio.prepare_request(methods.AUTH_REVOKE, payload, {}, {}, token)

        result['token'] = token
        assert isinstance(body, dict)
        assert body == result

    @pytest.mark.parametrize('payload,result', (
        (
            {'foo': 'bar'}, '{"foo": "bar"}'),
        (
            {'foo': 'bar', 'attachements': [{'a': 'b'}]},
            '{"foo": "bar", "attachements": [{"a": "b"}]}'
        ),
    ))
    def test_prepare_request_body_hook(self, token, payload, result):
        _, body, headers = sansio.prepare_request('https://hooks.slack.com/abcdefg', payload, {}, {}, token)

        assert body == result
        assert 'Authorization' in headers
        assert 'Content-type' in headers
        assert headers['Content-type'] == 'application/json; charset=utf-8'

    def test_prepare_request_body_message(self, token, message):
        _, body, headers = sansio.prepare_request(methods.AUTH_TEST, message, {}, {}, token)

        assert isinstance(body, str)
        assert 'Authorization' in headers
        assert 'Content-type' in headers
        assert headers['Content-type'] == 'application/json; charset=utf-8'

        _, body, headers = sansio.prepare_request(methods.AUTH_REVOKE, message, {}, {}, token)

        assert isinstance(body, dict)
        assert isinstance(body.get('attachments', ''), str)
        assert body['token'] == token

    def test_prepare_request_body_message_force_json(self, token, message):
        _, body, headers = sansio.prepare_request(methods.AUTH_REVOKE, message, {}, {}, token, as_json=True)

        assert isinstance(body, str)
        assert 'Authorization' in headers
        assert 'Content-type' in headers
        assert headers['Content-type'] == 'application/json; charset=utf-8'

    def test_prepare_request_message_hook(self, token, message):
        _, body, headers = sansio.prepare_request('https://hooks.slack.com/abcdefg', message, {}, {}, token)

        assert isinstance(body, str)
        data = json.loads(body)
        assert isinstance(data.get('attachments', []), list)
        assert 'Authorization' in headers
        assert 'Content-type' in headers
        assert headers['Content-type'] == 'application/json; charset=utf-8'

    @pytest.mark.parametrize('headers,global_headers,result', (
        ({'foo': 'bar', 'py': '3.7'}, {}, {'foo': 'bar', 'py': '3.7'}),
        ({'foo': 'bar', 'py': '3.7'}, {'sans': 'I/O'}, {'foo': 'bar', 'py': '3.7', 'sans': 'I/O'}),
        ({'foo': 'bar', 'py': '3.7'}, {'foo': 'baz', 'sans': 'I/O'}, {'foo': 'bar', 'py': '3.7', 'sans': 'I/O'})

    ))
    def test_prepare_request_headers(self, headers, global_headers, result):
        _, _, headers = sansio.prepare_request('', {}, headers, global_headers, '')
        assert headers == result

    def test_find_iteration(self):
        itermode, iterkey = sansio.find_iteration(methods.CHANNELS_LIST)
        assert itermode == methods.CHANNELS_LIST.value[1]
        assert iterkey == methods.CHANNELS_LIST.value[2]

    def test_find_iteration_custom_itermode(self):
        itermode, iterkey = sansio.find_iteration(methods.CHANNELS_LIST, itermode='timeline')
        assert itermode == 'timeline'
        assert iterkey == methods.CHANNELS_LIST.value[2]

    def test_find_iteration_custom_iterkey(self):
        itermode, iterkey = sansio.find_iteration(methods.CHANNELS_LIST, iterkey='users')
        assert itermode == methods.CHANNELS_LIST.value[1]
        assert iterkey == 'users'

    def test_find_iteration_not_found(self):
        with pytest.raises(ValueError):
            _, _ = sansio.find_iteration('')

    def test_find_iteration_wrong_mode(self):
        with pytest.raises(ValueError):
            _, _ = sansio.find_iteration('', itermode='python', iterkey='users')

    def test_prepare_iter_request(self):
        data, iterkey, itermode = sansio.prepare_iter_request(methods.CHANNELS_LIST, {})
        assert data == {'limit': 200}
        assert itermode == methods.CHANNELS_LIST.value[1]
        assert iterkey == methods.CHANNELS_LIST.value[2]

    def test_prepare_iter_request_no_iterkey(self):
        data, iterkey, itermode = sansio.prepare_iter_request(methods.CHANNELS_LIST, {})
        assert data == {'limit': 200}
        assert itermode == methods.CHANNELS_LIST.value[1]
        assert iterkey == methods.CHANNELS_LIST.value[2]

    def test_prepare_iter_request_cursor(self):
        data1, _, _ = sansio.prepare_iter_request('', {}, itermode='cursor', iterkey='channels', itervalue='abcdefg')
        assert data1 == {'limit': 200, 'cursor': 'abcdefg'}

        data2, _, _ = sansio.prepare_iter_request('', {}, itermode='cursor', itervalue='abcdefg', iterkey='channels',
                                                  limit=300)
        assert data2 == {'limit': 300, 'cursor': 'abcdefg'}

    def test_prepare_iter_request_page(self):
        data1, _, _ = sansio.prepare_iter_request('', {}, itermode='page', iterkey='channels', itervalue='abcdefg')
        assert data1 == {'count': 200, 'page': 'abcdefg'}

        data2, _, _ = sansio.prepare_iter_request('', {}, itermode='page', itervalue='abcdefg', iterkey='channels',
                                                  limit=300)
        assert data2 == {'count': 300, 'page': 'abcdefg'}

    def test_prepare_iter_request_timeline(self):
        data1, _, _ = sansio.prepare_iter_request('', {}, itermode='timeline', iterkey='channels', itervalue='abcdefg')
        assert data1 == {'count': 200, 'latest': 'abcdefg'}

        data2, _, _ = sansio.prepare_iter_request('', {}, itermode='timeline', itervalue='abcdefg', iterkey='channels',
                                                  limit=300)
        assert data2 == {'count': 300, 'latest': 'abcdefg'}


class TestResponse:
    def test_raise_for_status_200(self):
        try:
            sansio.raise_for_status(200, {}, {})
        except Exception as exc:
            raise pytest.fail('RAISE {}'.format(exc))

    def test_raise_for_status_400(self):
        with pytest.raises(exceptions.HTTPException):
            sansio.raise_for_status(400, {}, {})

    def test_raise_for_status_400_httpexception(self):
        with pytest.raises(exceptions.HTTPException) as exc:
            sansio.raise_for_status(400, {'test-header': 'hello'}, {'test-data': 'world'})

        assert exc.type == exceptions.HTTPException
        assert exc.value.status == 400
        assert exc.value.headers == {'test-header': 'hello'}
        assert exc.value.data == {'test-data': 'world'}

    def test_raise_for_status_429(self):
        with pytest.raises(exceptions.RateLimited) as exc:
            sansio.raise_for_status(429, {}, {})

        assert exc.type == exceptions.RateLimited
        assert exc.value.retry_after == 1

    def test_raise_for_status_429_headers(self):

        headers = {'Retry-After': '10'}

        with pytest.raises(exceptions.RateLimited) as exc:
            sansio.raise_for_status(429, headers, {})

        assert exc.type == exceptions.RateLimited
        assert exc.value.retry_after == 10

    def test_raise_for_status_429_wrong_headers(self):
        headers = {'Retry-After': 'aa'}

        with pytest.raises(exceptions.RateLimited) as exc:
            sansio.raise_for_status(429, headers, {})

        assert exc.type == exceptions.RateLimited
        assert exc.value.retry_after == 1

    def test_raise_for_api_error_ok(self):
        try:
            sansio.raise_for_api_error({}, {'ok': True})
        except Exception as exc:
            raise pytest.fail('RAISE {}'.format(exc))

    def test_raise_for_api_error_nok(self):

        data = {'ok': False}
        headers = {'test-header': 'hello'}

        with pytest.raises(exceptions.SlackAPIError) as exc:
            sansio.raise_for_api_error(headers, data)

        assert exc.type == exceptions.SlackAPIError
        assert exc.value.headers == {'test-header': 'hello'}
        assert exc.value.data == {'ok': False}
        assert exc.value.error == 'unknow_error'

    def test_raise_for_api_error_nok_with_error(self):

        data = {'ok': False, 'error': 'test_error'}

        with pytest.raises(exceptions.SlackAPIError) as exc:
            sansio.raise_for_api_error({}, data)

        assert exc.type == exceptions.SlackAPIError
        assert exc.value.error == 'test_error'

    def test_raise_for_api_error_warning(self, caplog):
        caplog.set_level(logging.WARNING)
        data = {'ok': True, 'warning': 'test warning'}
        sansio.raise_for_api_error({}, data)

        assert len(caplog.records) == 1
        assert caplog.records[0].msg == 'Slack API WARNING: %s'
        assert caplog.records[0].args == ('test warning',)

    def test_decode_body(self):
        body = b'hello world'
        decoded_body = sansio.decode_body({}, body)
        assert decoded_body == 'hello world'

    def test_decode_body_json(self):
        body = b'{"test-string":"hello","test-bool":true}'
        headers = {'content-type': 'application/json; charset=utf-8'}
        decoded_body = sansio.decode_body(headers, body)
        assert decoded_body == {"test-string": "hello", "test-bool": True}

    def test_decode_body_json_no_charset(self):
        body = b'{"test-string":"hello","test-bool":true}'
        headers = {'content-type': 'application/json'}
        decoded_body = sansio.decode_body(headers, body)
        assert decoded_body == {"test-string": "hello", "test-bool": True}

    def test_decode_response(self):
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = b'{"ok": true, "hello": "world"}'
        try:
            data = sansio.decode_response(200, headers, data)
        except Exception as exc:
            pytest.fail('RAISE {}'.format(exc))
        else:
            assert data == {'ok': True, 'hello': 'world'}

    def test_decode_iter_request_cursor(self):

        data = {'response_metadata': {'next_cursor': 'abcdefg'}}
        cursor = sansio.decode_iter_request(data)
        assert cursor == 'abcdefg'

    def test_decode_iter_request_paging(self):

        data = {'paging': {'page': 2, 'pages': 4}}
        page = sansio.decode_iter_request(data)
        assert page == 3

    def test_decode_iter_request_timeline(self):

        timestamp = time.time()
        latest = timestamp - 1000
        data = {'has_more': True,
                'latest': timestamp,
                'messages': [{'ts': latest}]}
        next_ = sansio.decode_iter_request(data)
        assert next_ == latest


class TestIncomingEvent:

    @pytest.mark.parametrize('event', ('bot', 'bot_edit'), indirect=True)
    def test_discard_event(self, event):
        assert sansio.discard_event(event, 'B0AAA0A00') is True

    def test_not_discard_event(self, event):
        assert sansio.discard_event(event, 'B0AAA0A01') is False

    def test_no_need_reconnect(self, event):
        assert sansio.need_reconnect(event) is False
