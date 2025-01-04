from dataclasses import dataclass, field
from typing import Literal

from coap_server.utils.constants import CoAPMethod


@dataclass(frozen=True)
class CoapRequest:
    """
    CoAP request data class.
    """
    method: Literal[CoAPMethod.GET, CoAPMethod.POST, CoAPMethod.PUT, CoAPMethod.DELETE]
    uri: str
    payload: bytes = field(repr=False)


def parse_request(data: bytes) -> CoapRequest:
    """
    Parse the CoAP request data and return a dictionary.

    :param data: CoAP request data
    :type data: bytes

    :return: CoAP request data as a dictionary
    :rtype: CoapRequest
    """
    raise NotImplementedError("parse_request function not implemented.")

