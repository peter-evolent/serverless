from serverless.wrappers import Request, Response

from tests import utils


class TestResponse:
    def test_response(self):
        resp = Response()
        result = resp.to_lambda_output()
        status_code, data = utils.parse_lambda_output(result)

        assert status_code == 200
        assert data == None
        assert isinstance(result['headers'], dict)

    def test_response_with_data(self, dict_data):
        resp = Response(dict_data)
        result = resp.to_lambda_output()
        status_code, data = utils.parse_lambda_output(result)

        assert status_code == 200
        assert data == dict_data

    def test_response_with_status_code(self):
        expected_status_code = 999

        resp = Response(None, expected_status_code)
        result = resp.to_lambda_output()
        status_code, data = utils.parse_lambda_output(result)

        assert status_code == expected_status_code
        assert data == None


class TestRequest:
    def test_request(self, context):
        event = utils.build_event(None)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict()
        assert req.query == dict()

    def test_request_with_data(self, dict_data, context):
        event = utils.build_event(dict_data)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict_data
        assert req.query == dict()

    def test_request_with_query(self, dict_data, context):
        event = utils.build_event(None, dict_data)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict()
        assert req.query == dict_data
