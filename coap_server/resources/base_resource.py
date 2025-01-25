from collections.abc import MutableMapping

from coap_server.utils.constants import CoapMessage


class BaseResource:
    """
    Base class for defining CoAP resources.

    This class should be inherited by all resources.
    Declares basic methods, that should be implemented by child classes.
    """

    objects: MutableMapping[int, MutableMapping[str, str | int]]

    def get(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("GET method not implemented.")

    def post(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("POST method not implemented.")

    def put(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("PUT method not implemented.")

    def delete(self, request: CoapMessage) -> CoapMessage:
        raise NotImplementedError("DELETE method not implemented.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(objects={self.objects})"
