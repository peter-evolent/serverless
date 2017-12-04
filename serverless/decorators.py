"""Serverless decorators"""
from functools import wraps

from serverless.exceptions import ServerlessError, InternalServerError
from serverless.wrappers import Request, Response


def lambda_handler(func):
    """
    A decorator for lambda handler that converts output of handler function
    to AWS Lambda response format. The wrapped handler function should return
    Response or Exception.
    """
    @wraps(func)
    def func_wrapper(event, context):
        req = Request(event, context)

        try:
            resp = func(req)
        except ServerlessError as e:
            status_code = e.status_code
            message = e.message if e.message else e.__class__.__name__
            data = {
                'message': message,
                'errors': e.errors
            }

            resp = Response(data, status_code)
        except Exception as e:
            # TODO: log e
            status_code = InternalServerError.status_code
            message = InternalServerError.__name__
            data = {
                'message': message,
                'errors': tuple()
            }

            resp = Response(data, status_code)
        return resp.to_lambda_output()
    return func_wrapper
