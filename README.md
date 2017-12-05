# Serverless

SDK for building a serverless App

```
from serverless import lambda_handler, Response, BadRequest

@lambda_handler
def handler(req):
    body_data_dict = req.data
    query_dict = req.query

    if 'expected_key' not in body_data_dict:
	raise BadRequest('expected_key is missing!')

    data_to_return = {
	'message': 'hello!'
    }
    return Response(data_to_return)

```

## Installation

This is a Python3.6 module available through public github repository

```
pip install -U git+https://github.com/peter-evolent/serverless.git
``` 

## Tests

To run the test suite, first install dev dependencies, then run pytes command
```
pip install -r requirements-dev.txt
pytest --cov=serverless
```

## License

This project is licensed under the Apache License 2.0  - see the [LICENSE](LICENSE) file for details
