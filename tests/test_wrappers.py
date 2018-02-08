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
from datetime import date, datetime
import uuid

import pytest

from serverless.wrappers import Request, Response
from serverless.exceptions import BadRequest

from tests import utils


class TestResponse:
    def test_response(self):
        resp = Response()
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert result.status_code == 200
        assert result.data == None
        assert isinstance(result.headers, dict)

    def test_response_with_data(self, dict_data):
        resp = Response(dict_data)
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert result.status_code == 200
        assert result.data == dict_data

    def test_response_with_date_data(self):
        date_obj = date(2018, 1, 1)
        resp = Response(date_obj)
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert result.data == '2018-01-01'

    def test_response_with_datetime_data(self):
        datetime_obj = datetime(2018, 1, 1,
            hour=1,
            minute=2,
            second=3,
            microsecond=45678
        )
        resp = Response(datetime_obj)
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert result.data == '2018-01-01T01:02:03.045678'

    def test_response_with_uuid_data(self):
        _id = uuid.uuid4()
        resp = Response(_id)
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert str(_id) in result.data

    def test_response_with_status_code(self):
        expected_status_code = 999

        resp = Response(None, expected_status_code)
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert result.status_code == expected_status_code
        assert result.data == None

    def test_response_with_headers(self, dict_data):
        resp = Response(headers=dict_data)
        lambda_output = resp.to_lambda_output()
        result = utils.parse_lambda_output(lambda_output)

        assert result.status_code == 200
        assert all([result.headers[k] == v for k, v in dict_data.items()])


class TestRequest:
    def test_request(self, context):
        event = utils.build_event(None)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict()
        assert req.query == dict()

    def test_request_with_invalid_json_data(self, context):
        invalid_json = 'This is not a json'
        event = {
            'body': invalid_json
        }
        req = Request(event, context)

        with pytest.raises(BadRequest):
            req.data

    def test_request_with_data(self, dict_data, context):
        event = utils.build_event(dict_data)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict_data
        assert req.query == dict()

    def test_request_with_query(self, dict_data, context):
        event = utils.build_event(None, query_params=dict_data)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict()
        assert req.query == dict_data

    def test_request_with_path_params(self, dict_data, context):
        event = utils.build_event(None, path_params=dict_data)
        req = Request(event, context)

        assert req.event == event
        assert req.context == context
        assert req.data == dict()
        assert req.params == dict_data
