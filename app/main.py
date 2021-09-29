from aiohttp import web
from aiohttp_swagger import setup_swagger

from config import logger
from routes import routes
from services.db.connect import db_pg_engine


app = web.Application()

app.cleanup_ctx.append(db_pg_engine)

app.add_routes(routes)

setup_swagger(app, swagger_url="/api/v1/doc")


def init_func(argv):
    """python -m aiohttp.web -H localhost -P 8000 main:init_func"""
    logger.info("INFO: Запуск сервера.")
    logger.info("==="*12)
    return app
