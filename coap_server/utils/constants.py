from enum import Enum

from coap_server.resources.base_resource import BaseResource


COAP_CODES = {
    '2.01': b"2.01 Created",
    '2.02': b"2.02 Deleted",
    '2.04': b"2.04 Changed",
    '2.05': b"2.05 Content",
    '4.04': b"4.04 Not Found",
    '4.05': b"4.05 Method Not Allowed",
}

# CoAP response codes
class CoAPCode(Enum):
    CREATED = '2.01'
    DELETED = '2.02'
    CHANGED = '2.04'
    CONTENT = '2.05'
    NOT_FOUND = '4.04'
    METHOD_NOT_ALLOWED = '4.05'

    @property
    def value(self):
        return COAP_CODES[self.name]


# CoAP methods
class CoAPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    @property
    def value(self):
        return self.name

    def get_resource_method(self, resource: BaseResource):
        if not hasattr(resource, self.value.lower()):
            raise AttributeError(f"Method {self.value} not allowed for this resource.")
        return getattr(resource, self.value.lower())
