import logging
from typing import MutableMapping

import typer

from coap_server.logger import logger
from coap_server.resources.base_resource import BaseResource
from coap_server.resources.sensors import SensorsResource
from coap_server.server import CoAPServer

app = typer.Typer()


@app.command()
def start(
    host: str = typer.Option("127.0.0.1", help="The host to connect to"),
    port: int = typer.Option(5683, help="The port to connect to"),
    verbose: int = typer.Option(
        2,
        "--verbose",
        "-v",
        count=True,
        help="Increase verbosity level (-v = warning, -vv = info, -vvv = debug)",
    ),
):
    """
    CoAP Server CLI.
    """

    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = log_levels[min(verbose, len(log_levels) - 1)]
    logger.setLevel(log_level)
    logger.info(f"Starting CoAP Server on {host}:{port}")

    routes: MutableMapping[str, BaseResource] = {
        "sensors": SensorsResource(
            {
                1: {"name": "Sensor 1", "temperature": 21},
                2: {"name": "Sensor 2", "temperature": 25},
            }
        ),
    }

    server = CoAPServer(routes, host, port)
    server.start()


app(prog_name="coap-server")
