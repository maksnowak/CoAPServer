from typing import Callable
from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.parser import encode_message, parse_message
from coap_server.resources.temperature_sensor import TemperatureSensorResource
from coap_server.resources.devices import DevicesResource


class RequestHandler:
    def __init__(self):
        self.routes = {
            "/temperature": TemperatureSensorResource(),
            "/devices": DevicesResource(),
        }

    def handle_request(self, data: bytes) -> bytes:
        request = parse_message(data)
        uri = request.uri
        resource = None

        for route, res in self.routes.items():
            if uri.startswith(route):
                resource = res
                break

        if not resource:
            return CoapCode.NOT_FOUND.value.encode("ascii")

        print(f"\nHandling request: {repr(request)}")
        try:
            method = self.get_resource_method(request, resource)
            response = method(request)
            return encode_message(response)
        except AttributeError:
            return CoapCode.METHOD_NOT_ALLOWED.value.encode("ascii")

    def get_resource_method(
        self, request: CoapMessage, resource: BaseResource
    ) -> Callable[[CoapMessage], CoapMessage]:
        if request.header_code == CoapCode.GET:
            return resource.get
        elif request.header_code == CoapCode.POST:
            return resource.post
        elif request.header_code == CoapCode.PUT:
            return resource.put

        # TODO: other methods

        raise AttributeError(
            f"Method {request.header_code} not allowed for this resource."
        )
