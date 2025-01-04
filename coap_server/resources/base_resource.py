from coap_server.utils.parser import CoapRequest


class BaseResource:
    """
    Base class for resources.

    This class should be inherited by all resources.
    It provides the basic methods that should be implemented by the child classes.
    """
    def get(self, request: CoapRequest) -> bytes:
        raise NotImplementedError("GET method not implemented.")

    def post(self, request: CoapRequest) -> bytes:
        raise NotImplementedError("POST method not implemented.")

    def put(self, request: CoapRequest) -> bytes:
        raise NotImplementedError("PUT method not implemented.")

    def delete(self, request: CoapRequest) -> bytes:
        raise NotImplementedError("DELETE method not implemented.")

