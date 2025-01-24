from typing import MutableMapping

import pytest

from coap_server.resources.base_resource import BaseResource
from coap_server.resources.sensors import SensorsResource


@pytest.fixture
def sensors() -> MutableMapping[int, MutableMapping[str, str | int]]:
    return {
        1: {
            "name": "sensor 1",
            "temperature": 21,
        },
        2: {
            "name": "sensor 2",
            "temperature": 25,
        },
    }


@pytest.fixture
def routes(sensors) -> MutableMapping[str, BaseResource]:
    return {
        "/sensors": SensorsResource(sensors),
    }
