from aiohttp import web
from aiohttp_swagger import swagger_path
from marshmallow import ValidationError

from config import settings
from services.db.models import UserTable
from services.db.queries import \
    get_user_query, save_user_query, delete_user_query, get_user_coordinates, get_users_inside_square
from services.db.serializer import simple_sqlalchemy_core_serializer
from views.user.schemas import UserUrlParamsSchema, SaveNewUserSchema, UserNeighborsSchema
from views.user.validators import save_user_validator, delete_user_validator


@swagger_path("views/user/swagger/get_user.yaml")
async def get_user(request):
    url_data = request.match_info

    try:
        validated_data = UserUrlParamsSchema().load(url_data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    user_id = validated_data['user_id']

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        current_user = await get_user_query(conn=conn, user_id=user_id)

        if current_user:
            serialized_user_data = simple_sqlalchemy_core_serializer(data=current_user, table=UserTable)
            return web.json_response(serialized_user_data)

    return web.Response(status=404, text="Пользователь не найден.")


@swagger_path("views/user/swagger/save_user.yaml")
async def save_user(request):
    data = await request.json()

    try:
        validated_data = SaveNewUserSchema().load(data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    username = validated_data['username']
    x = validated_data['x']
    y = validated_data['y']

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        await save_user_validator(conn=conn, username=username, x=x, y=y)
        await save_user_query(conn=conn, username=username, x=x, y=y)

        return web.Response(status=201, text="Пользователь успешно создан.")


@swagger_path("views/user/swagger/delete_user.yaml")
async def delete_user(request):
    url_data = request.match_info

    try:
        validated_data = UserUrlParamsSchema().load(url_data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    user_id = validated_data['user_id']

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        await delete_user_validator(conn=conn, user_id=user_id)
        await delete_user_query(conn=conn, user_id=user_id)

    return web.Response(status=204)


@swagger_path("views/user/swagger/get_user_neighbors.yaml")
async def get_user_neighbors(request):
    url_data = request.match_info
    rel_url_data = request.rel_url.query

    request_data = {}
    request_data.update(url_data)
    request_data.update(rel_url_data)

    try:
        validated_data = UserNeighborsSchema().load(request_data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    user_id = validated_data['user_id']
    radius = validated_data['radius']
    limit = validated_data['limit']

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        user_coordinates = await get_user_coordinates(conn=conn, user_id=user_id)

        if user_coordinates:
            user_x, user_y = user_coordinates.x, user_coordinates.y

            users = await get_users_inside_square(
                conn, user_id=user_id, x=user_x, y=user_y, radius=radius, limit=limit)

            all_users_in_circle = tuple(filter(lambda user: user.hypotenuse <= radius, users))
            all_sorted_users_in_circle = sorted(all_users_in_circle, key=lambda user: user.hypotenuse)

            response_data = []
            for user_row_proxy in all_sorted_users_in_circle:
                response_data.append(simple_sqlalchemy_core_serializer(data=user_row_proxy, table=UserTable))

            return web.json_response(response_data)

    return web.Response(status=404, text="Пользователь не найден.")
