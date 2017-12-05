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

from collections import namedtuple
import json


LambdaOutput = namedtuple('LambdaOutput', ['status_code', 'data', 'headers'])


def parse_lambda_output(output):
    """
    Parses AWS Lambda output and returns LambdaOutput

    Args:
        output (dict): an AWS Lambda compatible response

    Returns:
        result (LambdaOutput): parsed data 
    """
    status_code = output['statusCode']
    headers = output['headers']
    body = output['body']
    data = json.loads(body) if body else None

    return LambdaOutput(status_code, data, headers)

def build_event(body_data, query_data=dict()):
    """
    Builds AWS Lambda event using the provided data

    Args:
        body_data (dict): data loaded to the body of event
        query_data (dict): data loaded to query params of event

    Returns:
        event (dict): AWS Lambda event
    """
    body = json.dumps(body_data) if body_data else None
    event = {
        'body': body,
        'queryStringParameters': query_data
    }

    return event
