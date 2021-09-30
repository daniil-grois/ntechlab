from app.services.db.models import UserTable
from app.services.db.queries import get_users_inside_square
from app.services.db.serializer import simple_sqlalchemy_core_serializer
from app.views.user.dataclasses import NeighborsSearchParameters


async def get_user_neighbors_bl(conn, search_parameters: NeighborsSearchParameters):

    users = await get_users_inside_square(conn=conn, sp=search_parameters)

    all_users_in_circle = tuple(
        filter(lambda user: user.hypotenuse <= search_parameters.radius, users)
    )
    all_sorted_users_in_circle = sorted(
        all_users_in_circle, key=lambda user: user.hypotenuse
    )

    response_data = []
    for user_row_proxy in all_sorted_users_in_circle:
        response_data.append(
            simple_sqlalchemy_core_serializer(data=user_row_proxy, table=UserTable)
        )

    return response_data
