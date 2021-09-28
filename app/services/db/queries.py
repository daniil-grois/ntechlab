from typing import Optional, Tuple

from aiopg.sa.result import RowProxy
import aiopg.sa.connection as aiopg_conn
import sqlalchemy as sa
from sqlalchemy import func

from services.db.models import UserTable


async def get_user_coordinates(
    conn: aiopg_conn.SAConnection,
    user_id: int,
) -> Optional[Tuple[float]]:
    stmt = sa.select(UserTable.c.x, UserTable.c.y).where(UserTable.c.id == user_id)
    result = await conn.execute(stmt)
    re_fetchone = await result.fetchone()
    # TODO добавить условие
    return re_fetchone[0], re_fetchone[1]


async def get_users_inside_square(
    conn: aiopg_conn.SAConnection,
    user_id: int,
    x: float,
    y: float,
    radius: float,
    limit: int
):
    """"""
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



async def save_user(
    conn: aiopg_conn.SAConnection,
    username: str,
    x: float,
    y: float
) -> None:
    stmt = UserTable.insert().values(name=username, x=x, y=y)
    await conn.execute(stmt)


async def delete_user(
    conn: aiopg_conn.SAConnection,
    user_id: int
) -> None:
    stmt = UserTable.delete().where(UserTable.c.id == user_id)
    await conn.execute(stmt)
