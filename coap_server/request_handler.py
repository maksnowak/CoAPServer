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
            return b"4.04 Not Found"
        
        method = request.method.lower()
        if not hasattr(resource, method): # Check if the method is implemented in the resource
            return b"4.05 Method Not Allowed"
        
        print(f"Request: {repr(request)}")
        handler = getattr(resource, method)
        return handler(request)

