from typing import MutableMapping

import typer

from coap_server.resources.base_resource import BaseResource
from coap_server.resources.devices import DevicesResource
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

    routes: MutableMapping[str, BaseResource] = {
        "/devices": DevicesResource(
            {
                1: {
                    "name": "Device 1",
                    "temperature": 21,
                },
                2: {
                    "name": "Device 2",
                    "temperature": 25,
                },
            }
        ),
    }
    server = CoAPServer(routes, host, port)
    server.start()


app(prog_name="coap-server")
