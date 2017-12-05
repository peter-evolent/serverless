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

"""Serverless SDK"""
from functools import wraps
import logging

from serverless.exceptions import (
    ServerlessError, BadRequest, Unauthorized, Forbidden, NotFound, UnprocessableEntity
)
from serverless.wrappers import Request, Response


__version__ = '0.1'


log = logging.getLogger()


def lambda_handler(func):
    """
    A decorator for lambda handler that converts output of handler function
    to AWS Lambda response format. The wrapped handler function should return
    Response or Exception.
    """
    @wraps(func)
    def func_wrapper(event, context):
        """Wraps lambda handler function"""
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
            log.exception(e)
            status_code = 500
            message = 'InternalServerError'
            data = {
                'message': message,
                'errors': tuple()
            }

            resp = Response(data, status_code)
        return resp.to_lambda_output()
    return func_wrapper
