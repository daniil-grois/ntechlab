from typing import Optional, List

from aiopg.sa.result import RowProxy
import aiopg.sa.connection as aiopg_conn
import sqlalchemy as sa
from sqlalchemy import func

from services.db.models import UserTable


async def get_user_coordinates(
    conn: aiopg_conn.SAConnection,
    user_id: int,
) -> Optional[RowProxy]:
    stmt = sa.select(UserTable.c.x, UserTable.c.y).where(UserTable.c.id == user_id)
    result = await conn.execute(stmt)
    re_fetchone = await result.fetchone()

    if re_fetchone:
        return re_fetchone


async def get_user_query(
    conn: aiopg_conn.SAConnection,
    user_id: int,
) -> Optional[RowProxy]:
    stmt = sa.select(UserTable).where(UserTable.c.id == user_id)
    result = await conn.execute(stmt)
    re_fetchone = await result.fetchone()

    if re_fetchone:
        return re_fetchone


async def get_users_inside_square(
    conn: aiopg_conn.SAConnection,
    user_id: int,
    x: float,
    y: float,
    radius: float,
    limit: int
) -> List[RowProxy]:

    stmt = sa.select(
        UserTable, func.sqrt(
            func.pow(UserTable.c.x, 2) + func.pow(UserTable.c.y, 2)
        ).label("hypotenuse")
    ).where(
        sa.and_(
            sa.between(UserTable.c.x, x - radius, x + radius),
            sa.between(UserTable.c.y, y - radius, y + radius),
            UserTable.c.id != user_id
        )
    ).limit(limit)

    result = await conn.execute(stmt)
    re_fetchall = await result.fetchall()

    return re_fetchall


async def save_user_query(
    conn: aiopg_conn.SAConnection,
    username: str,
    x: float,
    y: float
) -> None:
    stmt = UserTable.insert().values(name=username, x=x, y=y)
    await conn.execute(stmt)


async def delete_user_query(
    conn: aiopg_conn.SAConnection,
    user_id: int
) -> None:
    stmt = UserTable.delete().where(UserTable.c.id == user_id)
    await conn.execute(stmt)


async def check_user_duplicate_coordinates(
    conn: aiopg_conn.SAConnection,
    x: float,
    y: float
) -> bool:
    stmt = sa.select([sa.exists().where(sa.and_(UserTable.c.x == x, UserTable.c.y == y))])

    result = await conn.execute(stmt)
    re_fetchone = await result.fetchone()

    return re_fetchone[0]


async def check_user_duplicate_username(
    conn: aiopg_conn.SAConnection,
    username: str,
) -> bool:
    stmt = sa.select([sa.exists().where(UserTable.c.name == username)])

    result = await conn.execute(stmt)
    re_fetchone = await result.fetchone()

    return re_fetchone[0]


async def user_exists_query(
    conn: aiopg_conn.SAConnection,
    user_id: int,
) -> bool:
    stmt = sa.select([sa.exists().where(UserTable.c.id == user_id)])

    result = await conn.execute(stmt)
    re_fetchone = await result.fetchone()

    return re_fetchone[0]
