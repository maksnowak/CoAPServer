import json
from typing import MutableMapping

from coap_server.logger import logger
from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
from coap_server.utils.construct_response import construct_response
from coap_server.utils.exceptions import (
    BadRequestError,
    MethodNotAllowedError,
    NotFoundError,
)


class SensorsResource(BaseResource):
    """
    CoAP resource representing sensors which can measure temperature.

    Example `objects` to be passed to constructor:
        objects = {
           1: {
               "name": "Sensor 1",
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
        """Validates the received sensor data."""

        keys = {"name", "temperature"}
        valid = set(data.keys()) == keys and isinstance(
            data["temperature"], int
        )

        if not valid:
            logger.warning(f"Validation failed for data: {data}")

        return valid

    def get(self, request: CoapMessage) -> CoapMessage:
        logger.info(f"Received GET request for URI: {request.uri}")

        match request.uri.strip("/").split("/"):
            case ["sensors"]:
                logger.debug("Returning all sensor data")
                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    json.dumps(self.objects).encode("ascii"),
                )

            case ["sensors", sensor_id_str]:
                try:
                    sensor_id = int(sensor_id_str)
                    obj = self.objects[sensor_id]
                    logger.debug(f"Returning data for sensor {sensor_id}")
                except (ValueError, KeyError):
                    logger.error(f"Sensor {sensor_id_str} not found")
                    raise NotFoundError

                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    json.dumps(obj).encode("ascii"),
                )

            case ["sensors", sensor_id_str, "temperature"]:
                try:
                    sensor_id = int(sensor_id_str)
                    obj = self.objects[sensor_id]
                    value = obj["temperature"]
                    logger.debug(
                        f"Returning temperature for sensor {sensor_id}: {value}"
                    )
                except (ValueError, KeyError):
                    logger.error(f"Sensor {sensor_id_str} not found")
                    raise NotFoundError

                response = construct_response(
                    request,
                    CoapCode.CONTENT,
                    str(value).encode("ascii"),
                )

            case _:
                logger.error(f"Invalid GET request path: {request.uri}")
                raise NotFoundError

        return response

    def post(self, request: CoapMessage) -> CoapMessage:
        logger.info(f"Received POST request for URI: {request.uri}")

        match request.uri.strip("/").split("/"):
            case ["sensors"]:
                try:
                    obj = json.loads(request.payload.decode())
                    logger.debug("Parsed request payload successfully")
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in request payload")
                    raise BadRequestError

                if not self.validate_data(obj):
                    raise BadRequestError

                new_id = max(self.objects.keys(), default=0) + 1
                self.objects[new_id] = obj

                logger.debug(f"Created new sensor {new_id}: {obj}")

                response = construct_response(
                    request, CoapCode.CREATED, json.dumps(obj).encode("ascii")
                )

            case ["sensors", _]:
                raise MethodNotAllowedError

            case ["sensors", _, "temperature"]:
                raise MethodNotAllowedError

            case _:
                logger.error(f"Invalid POST request path: {request.uri}")
                raise NotFoundError

        return response

    def put(self, request: CoapMessage) -> CoapMessage:
        logger.info(f"Received PUT request for URI: {request.uri}")

        match request.uri.strip("/").split("/"):
            case ["sensors", sensor_id_str]:
                try:
                    sensor_id = int(sensor_id_str)
                    obj = json.loads(request.payload.decode())
                    logger.debug(
                        f"Updating sensor {sensor_id} with data: {obj}"
                    )
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in request payload")
                    raise BadRequestError
                except ValueError:
                    logger.error(f"Invalid sensor ID: {sensor_id_str}")
                    raise NotFoundError

                if not self.validate_data(obj):
                    raise BadRequestError

                if sensor_id not in self.objects:
                    logger.error(f"Sensor {sensor_id} not found for update")
                    raise NotFoundError

                self.objects[sensor_id] = obj
                logger.debug(f"Updated sensor {sensor_id}")

                response = construct_response(
                    request, CoapCode.CHANGED, json.dumps(obj).encode("ascii")
                )

            case ["sensors", sensor_id_str, "temperature"]:
                try:
                    sensor_id = int(sensor_id_str)
                    new_temp = int(request.payload.decode())
                    logger.debug(
                        f"Updating temperature for sensor {sensor_id} to {new_temp}"
                    )
                except ValueError:
                    logger.error("Invalid temperature update format")
                    raise BadRequestError

                if sensor_id not in self.objects:
                    logger.error(f"Sensor {sensor_id} not found")
                    raise NotFoundError

                self.objects[sensor_id]["temperature"] = new_temp
                logger.debug(
                    f"Updated temperature for sensor {sensor_id}: {new_temp}"
                )

                response = construct_response(
                    request,
                    CoapCode.CHANGED,
                    json.dumps(self.objects[sensor_id]).encode("ascii"),
                )

            case _:
                logger.error(f"Invalid PUT request path: {request.uri}")
                raise NotFoundError

        return response

    def delete(self, request: CoapMessage) -> CoapMessage:
        logger.info(f"Received DELETE request for URI: {request.uri}")

        match request.uri.strip("/").split("/"):
            case ["sensors", sensor_id_str]:
                try:
                    sensor_id = int(sensor_id_str)
                except ValueError:
                    logger.error(f"Invalid sensor ID format: {sensor_id_str}")
                    raise NotFoundError

                if sensor_id not in self.objects:
                    logger.error(f"Sensor {sensor_id} not found for deletion")
                    raise NotFoundError

                self.objects.pop(sensor_id)
                logger.debug(f"Deleted sensor {sensor_id}")

                response = construct_response(request, CoapCode.DELETED, b"")

            case ["sensors", sensor_id, "temperature"]:
                raise MethodNotAllowedError

            case _:
                logger.error(f"Invalid DELETE request path: {request.uri}")
                raise NotFoundError

        return response
