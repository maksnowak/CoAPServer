import json
from typing import MutableMapping

from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.construct_response import construct_response
from coap_server.utils.exceptions import (
    BadRequestError,
    MethodNotAllowedError,
    NotFoundError,
)


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
                try:
                    device_id = int(device_id_str)
                except ValueError:
                    raise NotFoundError

                try:
                    obj = self.objects[device_id]
                except KeyError:
                    raise NotFoundError

                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    json.dumps(obj).encode("ascii"),
                )

            case ["devices", device_id_str, "temperature"]:
                try:
                    device_id = int(device_id_str)
                except ValueError:
                    raise NotFoundError

                try:
                    obj = self.objects[device_id]
                except KeyError:
                    raise NotFoundError

                value = obj["temperature"]

                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    str(value).encode("ascii"),
                )

            case _:
                raise NotFoundError

        return response

    def post(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                try:
                    obj = json.loads(request.payload.decode())
                except json.JSONDecodeError:
                    raise BadRequestError

                if not self.validate_data(obj):
                    raise BadRequestError

                ids = self.objects.keys()
                new_id = max(ids) + 1 if ids else 1
                self.objects[new_id] = obj

                response = construct_response(
                    request, CoapCode.CREATED, json.dumps(obj).encode("ascii")
                )

            case ["devices", device_id_str]:
                raise MethodNotAllowedError

            case ["devices", device_id_str, "temperature"]:
                raise MethodNotAllowedError

            case _:
                raise NotFoundError

        return response

    def put(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                raise MethodNotAllowedError

            case ["devices", device_id_str]:
                try:
                    device_id = int(device_id_str)
                except ValueError:
                    raise NotFoundError

                try:
                    obj = json.loads(request.payload.decode())
                except json.JSONDecodeError:
                    raise BadRequestError

                if not self.validate_data(obj):
                    raise BadRequestError

                if device_id not in self.objects.keys():
                    raise NotFoundError

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
                raise NotFoundError

        return response

    def delete(self, request: CoapMessage) -> CoapMessage:
        match request.uri.strip("/").split("/"):
            case ["devices"]:
                raise MethodNotAllowedError

            case ["devices", device_id_str]:
                try:
                    device_id = int(device_id_str)
                except ValueError:
                    raise NotFoundError

                if device_id not in self.objects:
                    raise NotFoundError

                self.objects.pop(device_id)

                response = construct_response(request, CoapCode.DELETED, b"")

            case ["devices", device_id, "temperature"]:
                raise MethodNotAllowedError

            case _:
                raise NotFoundError

        return response
