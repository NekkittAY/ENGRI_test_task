from aiohttp import web
from aiohttp.web import Response, Request
import hashlib
import json


async def healthcheck(request: Request) -> Response:
    """
    Health check function

    :request: request
    :return: Response
    """
    return web.json_response({}, status=200)


async def hash_string(request: Request) -> Response:
    """
    Hash string function

    :request: request
    :return: Response
    """
    try:
        data = await request.json()
        input_string = data.get('string')

        if not input_string:
            return web.json_response({'validation_errors': 'Field "string" is required'}, status=400)

        hashed_string = hashlib.sha256(input_string.encode()).hexdigest()
        return web.json_response({'hash_string': hashed_string}, status=200)
    except Exception:
        return web.json_response({'validation_errors': 'Invalid JSON format'}, status=400)


app = web.Application()

app.router.add_get('/healthcheck', healthcheck)
app.router.add_post('/hash', hash_string)

if __name__ == '__main__':
    web.run_app(app)
