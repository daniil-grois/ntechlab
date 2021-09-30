from aiohttp import web
from aiohttp_swagger import swagger_path


@swagger_path("app/views/common/swagger/healthcheck.yaml")
async def health_check(request):
    return web.Response(status=200, text="pong")
