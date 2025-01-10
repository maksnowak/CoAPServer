from coap_server.utils.constants import CoapMessage


class BaseResource:
    """
    Base class for resources.

    This class should be inherited by all resources.
    It provides the basic methods, that should be implemented by the child classes.
    """  # noqa: E501

    def get(self, message: CoapMessage) -> CoapMessage:
        raise NotImplementedError("GET method not implemented.")

    def post(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("POST method not implemented.")

    def put(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("PUT method not implemented.")

    def delete(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("DELETE method not implemented.")
