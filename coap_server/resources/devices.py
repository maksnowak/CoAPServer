import json
from typing import MutableMapping

from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.construct_response import construct_response


class DevicesResource(BaseResource):
    """
    CoAP resource representing devices with temperature sensors.

    objects = {
       device_id: {
           "name": "Device 1",
           "temperature": 21,
       },
       ...
    }
    """

    def __init__(
        self, objects: MutableMapping[int, MutableMapping[str, str | int]]
    ):
        self.objects = objects

    def validate_data(self, data: dict) -> bool:
        """Validates the received device data."""

        keys = {"name", "temperature"}
        return set(data.keys()) == keys and isinstance(
            data["temperature"], int
        )

    def get(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    json.dumps(self.objects).encode("ascii"),
                )

            case ["devices", device_id_str]:
                obj = self.objects[int(device_id_str)]

                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    json.dumps(obj).encode("ascii"),
                )

            case ["devices", device_id_str, "temperature"]:
                obj = self.objects[int(device_id_str)]
                value = obj["temperature"]

                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    str(value).encode("ascii"),
                )

            case _:
                raise ValueError

        return response

    def post(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                obj = json.loads(request.payload.decode())
                if not self.validate_data(obj):
                    raise ValueError  # TODO: bad req

                ids = self.objects.keys()
                new_id = max(ids) + 1 if ids else 1
                self.objects[new_id] = obj

                response = construct_response(
                    request, CoapCode.CREATED, json.dumps(obj).encode("ascii")
                )

            case ["devices", device_id_str]:
                raise AttributeError

            case ["devices", device_id_str, "temperature"]:
                raise AttributeError

            case _:
                raise ValueError

        return response

    def put(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                raise AttributeError

            case ["devices", device_id_str]:
                device_id = int(device_id_str)
                obj = json.loads(request.payload.decode())
                if not self.validate_data(obj):
                    raise ValueError  # TODO: bad req

                if device_id not in self.objects.keys():
                    raise ValueError

                self.objects[device_id] = obj

                response = construct_response(
                    request, CoapCode.CHANGED, json.dumps(obj).encode("ascii")
                )

            case ["devices", device_id, "temperature"]:
                device_id = int(device_id)
                value = int(request.payload.decode())

                self.objects[device_id]["temperature"] = value

                response = construct_response(
                    request,
                    CoapCode.CHANGED,
                    json.dumps(self.objects[device_id]).encode("ascii"),
                )

            case _:
                raise ValueError

        return response

    def delete(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                raise AttributeError

            case ["devices", device_id_str]:
                device_id = int(device_id_str)
                self.objects.pop(device_id)

                response = construct_response(request, CoapCode.DELETED, b"")

            case ["devices", device_id, "temperature"]:
                raise AttributeError

            case _:
                raise ValueError

        return response
