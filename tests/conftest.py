import pytest

from coap_server.resources.devices import DevicesResource
from coap_server.resources.temperature_sensor import TemperatureSensorResource


@pytest.fixture
def temperature():
    return {
        1: 22,
    }


@pytest.fixture
def devices():
    return {
        1: {
            "name": "Device 1",
        },
        2: {
            "name": "Device 2",
        },
    }


@pytest.fixture
def routes(temperature, devices):
    return {
        "/temperature": TemperatureSensorResource(temperature),
        "/devices": DevicesResource(devices),
    }
