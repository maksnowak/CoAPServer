from typing import Callable
from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.parser import encode_message, parse_message
from coap_server.resources.temperature_sensor import TemperatureSensorResource


class RequestHandler:
    def __init__(self):
        self.routes = {"/temperature": TemperatureSensorResource()}

    def handle_request(self, data: bytes) -> bytes:
        request = parse_message(data)
        uri = request.uri
        resource = None

        for route, res in self.routes.items():
            if uri.startswith(route):
                resource = res
                break

        if not resource:
            print("Resource not found")
            return encode_message(
                CoapMessage(
                    header_version=1,
                    header_type=0,
                    header_token_length=4,
                    header_code=CoapCode.NOT_FOUND,
                    header_mid=request.header_mid,
                    token=request.token,
                    options={},
                    payload=b"",
                )
            )

        print(f"\nHandling request: {repr(request)}")
        try:
            method = self.get_resource_method(request, resource)
            response = method(request)
            return encode_message(response)
        except AttributeError:
            return encode_message(
                CoapMessage(
                    header_version=1,
                    header_type=0,
                    header_token_length=4,
                    header_code=CoapCode.METHOD_NOT_ALLOWED,
                    header_mid=request.header_mid,
                    token=request.token,
                    options={},
                    payload=b"",
                )
            )

    def get_resource_method(
        self, request: CoapMessage, resource: BaseResource
    ) -> Callable[[CoapMessage], CoapMessage]:
        if request.header_code == CoapCode.GET:
            return resource.get

        if request.header_code == CoapCode.DELETE:
            return resource.delete

        # TODO: other methods

        raise AttributeError(
            f"Method {request.header_code} not allowed for this resource."
        )
