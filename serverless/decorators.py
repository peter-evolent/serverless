# -*- coding: utf-8 -*-
#
# Copyright 2017 Evolent Health, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Decorators for AWS Lambda handler functions"""
from functools import wraps
import logging

from serverless.wrappers import Request, Response
from serverless.exceptions import ServerlessError


def to_error_response(message, errors, status_code=500):
    """Returns Response created with the given message, errors, and status_code"""
    data = {
        'message': message,
        'errors': errors
    }

    return Response(data, status_code)


def lambda_handler(func):
    """
    A decorator for lambda handler that converts output of handler function
    to AWS Lambda response format. The wrapped handler function should return
    Response or Exception.

    Example:
        @lambda_handler
        def your_handler_func(req):
            # will receive req instead of raw event, context from lambda
            data = {
                'some key': 'value'
            }

            return Response(data, 203)

    Args:
        func (function): a handler function to be decorated

    Returns:
        func_wrapper (function): a wrapper function that is invoked via lambda

    Raises:
        TypeErorr: if event, context are not provided when invoking func_wrapper
    """
    logger = logging.getLogger(__name__)

    @wraps(func)
    def func_wrapper(event, context):
        """
        This is what's invoked via lambda.

        Args:
            event (dict): AWS Lambda event
            context (LambdaContext): AWS Lambda context

        .. _AWS Lambda python programming model:
           http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
        """
        req = Request(event, context)

        try:
            resp = func(req)

            if not isinstance(resp, Response):
                message = (
                    'Invalid return value from handler. '
                    'It should be either Response or Exception'
                )
                raise TypeError(message)
        except ServerlessError as e:
            status_code = e.status_code
            message = e.message if e.message else e.__class__.__name__

            resp = to_error_response(message, e.errors, status_code)
        except Exception as e:
            logger.exception(e)
            status_code = 500
            message = 'InternalServerError'
            errors = tuple()

            resp = to_error_response(message, errors, status_code)
        return resp.to_lambda_output()
    return func_wrapper
