from typing import Callable
from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoAPCode, CoapRequest
from coap_server.utils.parser import parse_request
from coap_server.resources.temperature_sensor import TemperatureSensorResource


class RequestHandler:
    def __init__(self):
        self.routes = {"/temperature": TemperatureSensorResource()}

    def handle_request(self, data: bytes) -> bytes:
        request = parse_request(data)
        resource = self.routes.get(request.uri)
        if not resource:
            return CoAPCode.NOT_FOUND.value

        print(f"Handling request: {repr(request)}")
        try:
            method = self.get_resource_method(request, resource)
            return method(request)
        except AttributeError:
            return CoAPCode.METHOD_NOT_ALLOWED.value

    def get_resource_method(
        self, request: CoapRequest, resource: BaseResource
    ) -> Callable[[CoapRequest], bytes]:
        if not hasattr(resource, request.method.value.lower()):
            raise AttributeError(
                f"Method {request.method.value} not allowed for this resource."
            )
        return getattr(resource, request.method.value.lower())
