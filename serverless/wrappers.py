"""Serverless wrapper classes"""
import json

from serverless.exceptions import BadRequest


class Request:
    """
    Request wrapper class to help precessing AWS Lambda input

    Args:
        event (dict): AWS Lambda event
        context (LambdaContext): AWS Lambda context

    Attributes:
        event (dict): AWS Lambda event
        context (LambdaContext): AWS Lambda context
        data (dict): request body
        query (dict): query string parameters

    Raises:
        BadRequest: if event['body'] is not None and not deserializable

    .. _AWS Lambda python programming model:
       http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
    """
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self._data = None

    # TODO: add pathParameters

    @property
    def data(self):
        """Returns HTTP body as dict"""
        if not self._data:
            body = self.event.get('body', None)
            try:
                self._data = json.loads(body) if body else dict()
            except json.JSONDecodeError as e:
                # TODO: check how to stringify this error,
                # https://docs.python.org/3/library/json.html#json.JSONDecodeError
                errors = (str(e))
                raise BadRequest('Malformed request body', errors)
        return self._data

    @property
    def query(self):
        """Returns HTTP query string as dict"""
        query_params = self.event.get('queryStringParameters', dict())

        return query_params


class Response:
    """
    Response wrapper class to help formmating output compatible with AWS Lambda

    Args:
        data (dict): data to populate response body
        status_code (int): response status code
        headers (dict): response headers
    """
    _security_headers = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'Cache-Control': 'no-cache, must-revalidate',
        'Pragma': 'no-cache',
        'X-XSS-Protection': '1; mode=block'
    }

    def __init__(self, data=None, status_code=200, headers=None):
        self.data = data
        self.status_code = status_code
        self._headers = headers if headers else dict()
        self.headers = {**self._security_headers, **self._headers}

    def to_lambda_output(self):
        """Returns dictionary compatiable with AWS Lambda output format"""
        body = json.dumps(self.data)
        resp = {
            'statusCode': self.status_code,
            'body': body,
            'headers': self.headers
        }

        return resp
