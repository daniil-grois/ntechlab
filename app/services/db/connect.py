from aiopg.sa import create_engine

from app.config import logger, settings


async def db_pg_engine(app):
    engine = await create_engine(
        host=settings.DB_CONFIG.DB_HOST,
        port=settings.DB_CONFIG.DB_PORT,
        database=settings.DB_CONFIG.DB_NAME,
        user=settings.DB_CONFIG.DB_USER,
        password=settings.DB_CONFIG.DB_PASS,
    )

    """Положим соединение с базой в экземпляр приложения чтобы иметь прямой доступ к базе из любой view"""
    app[settings.DB_CONFIG.DB_ENGINE_CONSTANT] = engine

    logger.info(f"INFO: DB '{settings.DB_CONFIG.DB_NAME}' connection established.")

    yield

    engine.close()
    await engine.wait_closed()
    logger.info(f"INFO: DB '{settings.DB_CONFIG.DB_NAME}' connection closed.")
