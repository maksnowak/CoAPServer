from dataclasses import dataclass
from enum import Enum


class CoapCode(Enum):
    EMPTY = "0.00"
    GET = "0.01"
    POST = "0.02"
    PUT = "0.03"
    DELETE = "0.04"
    FETCH = "0.05"
    PATCH = "0.06"
    IPATCH = "0.07"

    CREATED = "2.01"
    DELETED = "2.02"
    VALID = "2.03"
    CHANGED = "2.04"
    CONTENT = "2.05"
    CONTINUE = "2.31"

    BAD_REQUEST = "4.00"
    UNAUTHORIZED = "4.01"
    BAD_OPTION = "4.02"
    FORBIDDEN = "4.03"
    NOT_FOUND = "4.04"
    METHOD_NOT_ALLOWED = "4.05"
    NOT_ACCEPTABLE = "4.06"
    REQUEST_ENTITY_INCOMPLETE = "4.08"
    CONFLICT = "4.09"
    PRECONDITION_FAILED = "4.12"
    REQUEST_ENTITY_TOO_LARGE = "4.13"
    UNSUPPORTED_CONTENT_FORMAT = "4.15"

    INTERNAL_SERVER_ERROR = "5.00"
    NOT_IMPLEMENTED = "5.01"
    BAD_GATEWAY = "5.02"
    SERVICE_UNAVAILABLE = "5.03"
    GATEWAY_TIMEOUT = "5.04"
    PROXYING_NOT_SUPPORTED = "5.05"

    UNASSIGNED = "7.00"
    CSM = "7.01"
    PING = "7.02"
    PONG = "7.03"
    RELEASE = "7.04"
    ABORT = "7.05"


class CoapOption(Enum):
    IF_MATCH = 1
    URI_HOST = 3
    ETAG = 4
    IF_NONE_MATCH = 5
    URI_PORT = 7
    LOCATION_PATH = 8
    URI_PATH = 11
    CONTENT_FORMAT = 12
    MAX_AGE = 14
    URI_QUERY = 15
    ACCEPT = 17
    LOCATION_QUERY = 20
    PROXY_URI = 35
    PROXY_SCHEME = 39
    SIZE1 = 60


@dataclass(frozen=True)
class CoapMessage:
    """
    CoAP message data class.
    """

    header_version: int
    header_type: int
    header_token_length: int
    header_code: CoapCode
    header_mid: int
    token: bytes
    options: dict[CoapOption, bytes]
    payload: bytes

    @property
    def uri(self) -> str:
        """
        Compose the URI from the options.
        """

        value = ""
        if CoapOption.URI_PATH in self.options:
            value += "/".join(self.options[CoapOption.URI_PATH].decode().split(","))
        if CoapOption.URI_QUERY in self.options:
            value += "?" + "&".join(
                self.options[CoapOption.URI_QUERY].decode().split(",")
            )
        return value
