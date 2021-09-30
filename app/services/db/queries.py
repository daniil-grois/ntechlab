from typing import List, Optional

import aiopg.sa.connection as aiopg_conn
import sqlalchemy as sa
from aiopg.sa.result import RowProxy
from sqlalchemy import func

from app.services.db.models import UserTable
from app.views.user.dataclasses import NeighborsSearchParameters, Coordinates


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
    sp: NeighborsSearchParameters,
) -> List[RowProxy]:

    stmt = (
        sa.select(
            UserTable,
            func.sqrt(func.pow(UserTable.c.x, 2) + func.pow(UserTable.c.y, 2)).label(
                "hypotenuse"
            ),
        )
        .where(
            sa.and_(
                sa.between(
                    UserTable.c.x,
                    sp.user_coordinates.x - sp.radius,
                    sp.user_coordinates.x + sp.radius,
                ),
                sa.between(
                    UserTable.c.y,
                    sp.user_coordinates.y - sp.radius,
                    sp.user_coordinates.y + sp.radius,
                ),
                UserTable.c.id != sp.user_id,
            )
        )
        .limit(sp.limit)
    )

    result = await conn.execute(stmt)
    re_fetchall = await result.fetchall()

    return re_fetchall


async def save_user_query(
    conn: aiopg_conn.SAConnection, username: str, user_coordinates: Coordinates
) -> None:
    stmt = UserTable.insert().values(name=username, x=user_coordinates.x, y=user_coordinates.y)
    await conn.execute(stmt)


async def delete_user_query(
    conn: aiopg_conn.SAConnection, user_id: int
) -> None:
    stmt = UserTable.delete().where(UserTable.c.id == user_id)
    await conn.execute(stmt)


async def check_user_duplicate_coordinates(
    conn: aiopg_conn.SAConnection, user_coordinates: Coordinates
) -> bool:
    stmt = sa.select(
        [sa.exists().where(sa.and_(UserTable.c.x == user_coordinates.x, UserTable.c.y == user_coordinates.y))]
    )
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
