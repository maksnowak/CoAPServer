from coap_server.server import CoAPServer
import typer

app = typer.Typer()

@app.command()
def start(
    host: str = typer.Option("127.0.0.1", help="The host to connect to"),
    port: int = typer.Option(5683, help="The port to connect to"),
):
    """
    CLI for CoAP server.
    """
    server = CoAPServer(host, port)
    server.start()

app(prog_name="coap-server")

