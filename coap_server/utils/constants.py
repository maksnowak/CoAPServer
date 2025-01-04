from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


# CoAP methods
class CoAPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    @property
    def value(self):
        return self.name

    @staticmethod
    def from_str(method: str) -> "CoAPMethod":
        return CoAPMethod[method.upper()]


# CoAP request
@dataclass(frozen=True)
class CoapRequest:
    """
    CoAP request data class.
    """

    method: Literal[CoAPMethod.GET, CoAPMethod.POST, CoAPMethod.PUT, CoAPMethod.DELETE]
    uri: str
    payload: bytes = field(repr=False)


COAP_CODES = {
    "2.01": b"2.01 Created",
    "2.02": b"2.02 Deleted",
    "2.04": b"2.04 Changed",
    "2.05": b"2.05 Content",
    "4.04": b"4.04 Not Found",
    "4.05": b"4.05 Method Not Allowed",
}


# CoAP response codes
class CoAPCode(Enum):
    CREATED = "2.01"
    DELETED = "2.02"
    CHANGED = "2.04"
    CONTENT = "2.05"
    NOT_FOUND = "4.04"
    METHOD_NOT_ALLOWED = "4.05"

    @property
    def value(self):
        return COAP_CODES[self.name]
