from coap_server.utils.constants import CoAPCode
from coap_server.utils.parser import parse_request
from resources.temperature_sensor import TemperatureSensorResource

class RequestHandler:
    def __init__(self):
        self.routes = {
            '/temperature': TemperatureSensorResource()
        }

    def handle_request(self, data: bytes) -> bytes:
        request = parse_request(data)
        resource = self.routes.get(request.uri)
        if not resource:
            return CoAPCode.NOT_FOUND.value
        
        print(f"Handling request: {repr(request)}")
        try:
            method = request.method.get_resource_method(resource)
            return method(request)
        except AttributeError:
            return CoAPCode.METHOD_NOT_ALLOWED.value

