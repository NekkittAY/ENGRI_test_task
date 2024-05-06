import json
import pytest
from aiohttp import web
import hashlib

from main import healthcheck, hash_string


@pytest.fixture
def test_client(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash_string)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.mark.asyncio
async def test_healthcheck(test_client):
    resp = await test_client.get('/healthcheck')
    assert resp.status == 200
    await test_client.close()


@pytest.mark.asyncio
async def test_hash_string_valid_input(test_client):
    input_data = {'string': 'test_string'}
    resp = await test_client.post('/hash', json=input_data)
    assert resp.status == 200
    data = await resp.json()
    assert 'hash_string' in data


@pytest.mark.asyncio
async def test_hash_string_missing_input(test_client):
    input_data = {}
    resp = await test_client.post('/hash', json=input_data)
    assert resp.status == 400
    data = await resp.json()
    assert 'validation_errors' in data
    assert data['validation_errors'] == 'Field "string" is required'


@pytest.mark.asyncio
async def test_hash_string_invalid_json(test_client):
    invalid_json = '{"key": "value" }'
    resp = await test_client.post('/hash', json=invalid_json)
    assert resp.status == 400
    data = await resp.json()
    assert 'validation_errors' in data
    assert data['validation_errors'] == 'Invalid JSON format'
