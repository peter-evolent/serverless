# Serverless

SDK for building a serverless App.


```python
from serverless import lambda_handler, Response, BadRequest

@lambda_handler
def handler(req):
    # once decorated, handler will receive Request object as its argument.
    # Request object has data, query attributes to access HTTP Request body and query strings
    body_data_dict = req.data
    query_dict = req.query
    path_params_dict = req.params

    if 'expected_key' not in body_data_dict:
        # Raise serverless Exceptions, and response will be automatically generated.
        # For example, below exception will create response 400 response

        raise BadRequest('expected_key is missing!')

    data_to_return = {
        'message': 'hello!'
    }

    # When you are done, you should return Response
    return Response(data_to_return)
```


## lambda_handler

This is a main decorator for lambda handler function, and it provides the following features:

- Request will be passed to the handler function
- Will be using Response to format the output
- Predefined can be used to handle both server and client side errors

## Request

This class holds incoming request data, and it will be passed to the handler.
NOTE: `data` and `query` attributes will always return dict

Attributes:
- data: JSON Body as dict
- query: Query string params as dict
- params: Path params as dict
- event: AWS Lambda event
- context: AWS Lambda context

## Response

This is the helper class that you will use to return data to the end user.
In addition to the native data types, it also supports `date`, `datetime`, and `UUID` types.
The following security headers will be used by default,

```python
{
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'Cache-Control': 'no-cache, must-revalidate',
    'Pragma': 'no-cache',
    'X-XSS-Protection': '1; mode=block'
}
```

Check the example codes below for how to create a response

```python
some_data = {'score': 20}
status_code = 203

# creating 200 response with data
resp = Response(data=some_data)

# creating response with data and custom status_code
resp = Response(data=some_data, status_code=some_data)

# creating response with data, status_code, and headers
custom_header = {
    'X-Custom-Header': 'value'
}
resp = Response(data=some_data, status_code=status_code, headers=custom_header)
```


## Error Handling

Serverless ships predefined client and server exceptions that you can use.

```python

from serverless import lambda_handler, Response, BadRequest

@lamda_handler
def handler(req):
    if 'user_id' not in req.data:
        raise BadRequest('Invalid data')
    
    return Response(req.event)


"""
excepted output (if user_id key not found in req.data): 

HTTP/1.1 400 Bad Request
{
    "errors": [],
    "message": "Invalid data"
}
"""
```

Server errors(5XX):
- ServerlessError

Client errors(4XX):
- BadRequest(400)
- Unauthorized(401)
- Forbidden(403)
- NotFound(404)
- UnprocessableEntity(422)

Any other exceptions raised from the handler will be mapped to ServerlessError.

## Installation

This is a Python3.6 module available through public github repository.

1. add `git+https://github.com/peter-evolent/serverless.git@master` to requirement.txt
2. run `pip install -r requirements.txt`

## Tests

To run the test suite, first install dev dependencies, then run pytes command
```
pip install -r requirements-dev.txt
pytest --cov=serverless -v
```

## Todo

- support list of error details

## License

This project is licensed under the Apache License 2.0  - see the [LICENSE](LICENSE) file for details
