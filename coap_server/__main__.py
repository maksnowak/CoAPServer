import typer

from coap_server.resources.devices import DevicesResource
from coap_server.resources.temperature_sensor import TemperatureSensorResource
from coap_server.server import CoAPServer

app = typer.Typer()


@app.command()
def start(
    host: str = typer.Option("127.0.0.1", help="The host to connect to"),
    port: int = typer.Option(5683, help="The port to connect to"),
):
    """
    CLI for CoAP server.
    """

    routes = {
        "/devices": DevicesResource(
            {
                1: {"name": "Device 1"},
            }
        ),
        "/temperature": TemperatureSensorResource(
            {
                1: 22,
            }
        ),
    }
    server = CoAPServer(routes, host, port)
    server.start()


app(prog_name="coap-server")
