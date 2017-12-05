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

from serverless.decorators import lambda_handler
from serverless.wrappers import Response
from serverless.exceptions import BadRequest

from tests import utils


def test_lambda_handler(context):
    event = utils.build_event(None)

    @lambda_handler
    def handler(req):
        payload = {
            'event': req.event,
            'context': req.context
        }

        return Response(payload)

    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == 200
    assert result.data['event'] == event
    assert result.data['context'] == context

def test_lambda_handler_invalid_return_value(context):
    event = utils.build_event(None)

    @lambda_handler
    def handler(req):
        return None

    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == 500

def test_lambda_handler_with_data(context, dict_data):
    event = utils.build_event(dict_data)

    @lambda_handler
    def handler(req):
        payload = {
            'req_data': req.data
        }

        return Response(payload)

    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == 200
    assert result.data['req_data'] == dict_data

def test_lambda_handler_with_query(context, dict_data):
    event = utils.build_event(None, dict_data)

    @lambda_handler
    def handler(req):
        payload = {
            'req_query': req.query
        }

        return Response(payload)

    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == 200
    assert result.data['req_query'] == dict_data

def test_lambda_handler_with_status_code(context):
    expected_status_code = 999
    event = utils.build_event(None)

    @lambda_handler
    def handler(req):
        return Response(None, expected_status_code)

    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == expected_status_code
    assert not result.data

def test_lambda_handler_exception(context):
    event = utils.build_event(None)

    @lambda_handler
    def handler(req):
        raise Exception('unknown exception')
    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == 500
    assert 'message' in result.data
    assert 'errors' in result.data

def test_lambda_handler_bad_request(context):
    event = utils.build_event(None)

    @lambda_handler
    def handler(req):
        raise BadRequest('invalid request')
    lambda_output = handler(event, context)
    result = utils.parse_lambda_output(lambda_output)

    assert result.status_code == BadRequest.status_code
    assert 'message' in result.data
    assert 'errors' in result.data
