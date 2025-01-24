from typing import MutableMapping

import pytest

from coap_server.resources.base_resource import BaseResource
from coap_server.resources.devices import DevicesResource


@pytest.fixture
def devices() -> MutableMapping[int, MutableMapping[str, str | int]]:
    return {
        1: {
            "name": "Device 1",
            "temperature": 21,
        },
        2: {
            "name": "Device 2",
            "temperature": 25,
        },
    }


@pytest.fixture
def routes(devices) -> MutableMapping[str, BaseResource]:
    return {
        "/devices": DevicesResource(devices),
    }
