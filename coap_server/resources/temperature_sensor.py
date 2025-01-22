from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage


class TemperatureSensorResource(BaseResource):
    def __init__(self):
        self.sensors = {1: 22}  # {sensor_id: temperature}

    def get(self, request: CoapMessage) -> CoapMessage:
        response = CoapMessage(
            header_version=request.header_version,
            header_type=request.header_type,
            header_token_length=request.header_token_length,
            header_code=CoapCode.CONTENT,
            header_mid=request.header_mid,
            token=request.token,
            options={},
            payload=b"Current temperature is 22C",
        )

        return response

    def delete(self, request: CoapMessage) -> CoapMessage:
        sensor_id = int(request.uri.split("/")[-1])
        if sensor_id not in self.sensors:
            return CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.NOT_FOUND,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b"Sensor not found",
            )

        self.sensors.pop(sensor_id, None)
        response = CoapMessage(
            header_version=request.header_version,
            header_type=request.header_type,
            header_token_length=request.header_token_length,
            header_code=CoapCode.DELETED,
            header_mid=request.header_mid,
            token=request.token,
            options={},
            payload=b"Sensor deleted",
        )

        return response
