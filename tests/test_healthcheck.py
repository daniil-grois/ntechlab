import pytest
from aiohttp import web
from app.views.common.views import health_check


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/', health_check)
    return loop.run_until_complete(aiohttp_client(app))


async def test_get_value(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'pong'
