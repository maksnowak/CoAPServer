import json
from typing import Callable, MutableMapping

from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.construct_response import construct_response
from coap_server.utils.parser import encode_message, parse_message


class RequestHandler:
    def __init__(self, routes: MutableMapping[str, BaseResource]):
        # routes = {
        #     "/name": Resource(),
        #     ...
        # }
        self.routes = routes

    def handle_request(self, data: bytes) -> bytes:
        request = parse_message(data)
        print(f"\nHandling request: {repr(request)}")

        try:
            for route, res in self.routes.items():
                if request.uri.startswith(route):
                    resource = res
                    break
            else:
                raise ValueError

            method = self.get_resource_method(request, resource)
            response = method(request)

        except AttributeError:
            response = construct_response(
                request,
                CoapCode.METHOD_NOT_ALLOWED,
                json.dumps(
                    {"error": "Method not allowed for this resource"}
                ).encode("ascii"),
            )

        except json.JSONDecodeError:
            response = construct_response(
                request,
                CoapCode.BAD_REQUEST,
                json.dumps({"error": "Invalid payload"}).encode("ascii"),
            )

        except (ValueError, KeyError):
            response = construct_response(
                request,
                CoapCode.NOT_FOUND,
                json.dumps({"error": f"Not found: {request.uri}"}).encode(
                    "ascii"
                ),
            )

        return encode_message(response)

    def get_resource_method(
        self, request: CoapMessage, resource: BaseResource
    ) -> Callable[[CoapMessage], CoapMessage]:
        if request.header_code == CoapCode.GET:
            return resource.get
        elif request.header_code == CoapCode.POST:
            return resource.post
        elif request.header_code == CoapCode.PUT:
            return resource.put
        elif request.header_code == CoapCode.DELETE:
            return resource.delete

        raise AttributeError(
            f"Method {request.header_code} not allowed for this resource."
        )
