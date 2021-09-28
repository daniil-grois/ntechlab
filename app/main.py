import asyncio

from aiohttp import web
from config import logger
from routes import routes
from services.db.connect import db_pg_engine


app = web.Application()

app.cleanup_ctx.append(db_pg_engine)

app.add_routes(routes)

# if settings.ENV_FOR_DYNACONF != 'production':
#     import aiohttp_cors
#     from config import default_cors
#
#     cors = aiohttp_cors.setup(app, defaults=default_cors)
#     for route in list(app.router.routes()):
#         cors.add(route)


def init_func(argv):
    """python -m aiohttp.web -H localhost -P 8000 main:init_func"""
    logger.info("INFO: Запуск сервера.")
    logger.info("==="*12)
    return app

