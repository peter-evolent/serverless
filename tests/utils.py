import json


def parse_lambda_output(output):
    """
    Parses AWS Lambda output and returns status_code and body as tuple

    Args:
        output (dict): an AWS Lambda compatible response

    Returns:
        result (tuple): status_code (int), data (dict) 
    """
    status_code = output['statusCode']
    body = output['body']
    data = json.loads(body) if body else None

    return status_code, data

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
