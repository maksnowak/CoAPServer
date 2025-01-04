from coap_server.resources.base_resource import BaseResource

class TemperatureSensorResource(BaseResource):
    def __init__(self):
        self.sensors = {}  # {sensor_id: temperature}

    def get(self, request):
        return b"2.05 Content: Current temperature is 22C"

    def post(self, request):
        return b"2.01 Created"

    def put(self, request):
        return b"2.04 Changed"

    def delete(self, request):
        return b"2.02 Deleted"

