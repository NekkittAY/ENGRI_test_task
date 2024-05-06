import click
from aiohttp import web
from aiohttp.web import Request, Response

from main import app


@click.command()
@click.option('--host', default='0.0.0.0', help='Host for the server')
@click.option('--port', default=8080, help='Port for the server')
def run_server(host, port):
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    run_server()
