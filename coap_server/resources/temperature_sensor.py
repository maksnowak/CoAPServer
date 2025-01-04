from coap_server.resources.base_resource import BaseResource
from coap_server.utils.parser import CoapRequest

class TemperatureSensorResource(BaseResource):
    def __init__(self):
        self.sensors = {}  # {sensor_id: temperature}

    def get(self, request: CoapRequest):
        return b"2.05 Content: Current temperature is 22C"

    def post(self, request: CoapRequest):
        return b"2.01 Created"

    def put(self, request: CoapRequest):
        return b"2.04 Changed"

    def delete(self, request: CoapRequest):
        return b"2.02 Deleted"

