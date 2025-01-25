import json
from typing import Callable, MutableMapping

from coap_server.logger import logger
from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.construct_response import construct_response
from coap_server.utils.exceptions import (
    BadRequestError,
    MethodNotAllowedError,
    NotFoundError,
)
from coap_server.utils.parser import encode_message, parse_message


class RequestHandler:
    """
    Handles incoming CoAP requests by routing them to the appropriate resource.

    Structure of `routes` to be passed to constructor:
        routes = {
            "name": Resource(),
            ...
        }
    """

    def __init__(self, routes: MutableMapping[str, BaseResource]):
        self.routes = routes

    def handle_request(self, data: bytes) -> bytes:
        request = parse_message(data)
        logger.debug(f"Handling request: {repr(request)}")

        try:
            for route, res in self.routes.items():
                if request.uri.lstrip("/").startswith(route):
                    resource = res
                    break
            else:
                raise NotFoundError

            method = self.get_resource_method(request, resource)
            response = method(request)
            logger.info(f"Request to {request.uri} handled successfully")

        except MethodNotAllowedError:
            logger.warning(f"Method not allowed for {request.uri}")
            response = construct_response(
                request,
                CoapCode.METHOD_NOT_ALLOWED,
                json.dumps(
                    {"error": "Method not allowed for this resource"}
                ).encode("ascii"),
            )

        except NotFoundError:
            logger.warning(f"Resource not found: {request.uri}")
            response = construct_response(
                request,
                CoapCode.NOT_FOUND,
                json.dumps({"error": f"Not found: {request.uri}"}).encode(
                    "ascii"
                ),
            )

        except BadRequestError:
            logger.error(f"Bad request: {request.uri}")
            response = construct_response(
                request,
                CoapCode.BAD_REQUEST,
                json.dumps({"error": "Invalid payload"}).encode("ascii"),
            )

        except Exception as e:
            logger.critical(f"Unexpected error: {repr(e)}")
            response = construct_response(
                request,
                CoapCode.BAD_REQUEST,
                json.dumps({"error": repr(e)}).encode("ascii"),
            )

        return encode_message(response)

    def get_resource_method(
        self, request: CoapMessage, resource: BaseResource
    ) -> Callable[[CoapMessage], CoapMessage]:
        """Returns the appropriate resource method based on the CoAP request method code."""

        if request.header_code == CoapCode.GET:
            return resource.get
        elif request.header_code == CoapCode.POST:
            return resource.post
        elif request.header_code == CoapCode.PUT:
            return resource.put
        elif request.header_code == CoapCode.DELETE:
            return resource.delete

        raise MethodNotAllowedError
