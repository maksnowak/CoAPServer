from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption


class TemperatureSensorResource(BaseResource):
    def __init__(self, sensors: dict[int, int]):
        # sensors = {
        #     sensor_id: temperature,
        #     ...
        # }
        self.sensors = sensors

    def get(self, request: CoapMessage) -> CoapMessage:
        sensor_id = int(
            request.options.get(CoapOption.URI_PATH, b"-1").decode().rsplit("/", 1)[-1]
        )
        if sensor_id not in self.sensors.keys():
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

        temperature = self.sensors.get(sensor_id, None)
        payload = f"Temperature is {temperature}C".encode()
        response = CoapMessage(
            header_version=request.header_version,
            header_type=request.header_type,
            header_token_length=request.header_token_length,
            header_code=CoapCode.CONTENT,
            header_mid=request.header_mid,
            token=request.token,
            options={},
            payload=payload,
        )

        return response

    def delete(self, request: CoapMessage) -> CoapMessage:
        sensor_id = int(
            request.options.get(CoapOption.URI_PATH, b"-1").decode().rsplit("/", 1)[-1]
        )
        if sensor_id not in self.sensors.keys():
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

    def __repr__(self) -> str:
        return f"TemperatureSensorResource(sensors={self.sensors})"
