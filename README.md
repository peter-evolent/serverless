# Serverless

SDK for building a serverless App.


```
from serverless import lambda_handler, Response, BadRequest

@lambda_handler
def handler(req):
    # once decorated, handler will receive Request object as its argument.
    # Request object has data, query attributes to access HTTP Request body and query strings

    body_data_dict = req.data
    query_dict = req.query

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

## Installation

This is a Python3.6 module available through public github repository.


```
pip install -U git+https://github.com/peter-evolent/serverless.git@master
```

## Tests

To run the test suite, first install dev dependencies, then run pytes command
```
pip install -r requirements-dev.txt
pytest --cov=serverless -v
```

## License

This project is licensed under the Apache License 2.0  - see the [LICENSE](LICENSE) file for details
