import aiopg.sa.connection as aiopg_conn

from exceptions.user import UserDuplicateCoordinatesError, UserDuplicateNameError, UserDoesNotExistError
from services.db.queries import check_user_duplicate_coordinates, check_user_duplicate_username, user_exists_query


async def save_user_validator(
    conn: aiopg_conn.SAConnection,
    username: str,
    x: float,
    y: float
) -> None:
    """Проверка на 500 ошибки функции сохранения пользователя."""

    """Проверим, что пользователя с такими координатами еще не существует"""
    existing_duplicate_coord = await check_user_duplicate_coordinates(conn=conn, x=x, y=y)
    if existing_duplicate_coord:
        raise UserDuplicateCoordinatesError

    """Проверим, что имя пользователя не повторяется"""
    existing_duplicate_username = await check_user_duplicate_username(conn=conn, username=username)
    if existing_duplicate_username:
        raise UserDuplicateNameError

    return


async def delete_user_validator(
    conn: aiopg_conn.SAConnection,
    user_id: int,
) -> None:
    """Проверка на 500 ошибки функции удаления пользователя."""

    """Проверим, что такой пользователь существует"""
    existing_user = await user_exists_query(conn=conn, user_id=user_id)
    if not existing_user:
        raise UserDoesNotExistError

    return
