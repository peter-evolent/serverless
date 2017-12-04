import json
import pytest

from tests import utils


@pytest.fixture
def dict_data():
    return {
        'k1': str(),
        'k2': int(),
        'k3': list(),
        'k4': dict()
    }

@pytest.fixture
def context():
    return None
