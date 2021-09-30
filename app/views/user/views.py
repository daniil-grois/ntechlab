import json

from aiohttp import web
from aiohttp_swagger import swagger_path
from marshmallow import ValidationError

from app.bl.user import get_user_neighbors_bl
from app.config import settings
from app.services.db.models import UserTable
from app.services.db.queries import (
    delete_user_query,
    get_user_coordinates,
    get_user_query,
    save_user_query,
)
from app.services.db.serializer import simple_sqlalchemy_core_serializer
from app.utils import DecimalEncoder
from app.views.user.dataclasses import Coordinates, NeighborsSearchParameters
from app.views.user.schemas import (
    SaveNewUserSchema,
    UserNeighborsSchema,
    UserUrlParamsSchema,
)
from app.views.user.validators import delete_user_validator, save_user_validator


@swagger_path("app/views/user/swagger/get_user.yaml")
async def get_user(request):
    url_data = request.match_info

    try:
        validated_data = UserUrlParamsSchema().load(url_data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    user_id = validated_data["user_id"]

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        current_user = await get_user_query(conn=conn, user_id=user_id)

        if current_user:
            serialized_user_data = simple_sqlalchemy_core_serializer(
                data=current_user, table=UserTable
            )
            return web.json_response(serialized_user_data)

    return web.Response(status=404, text="Пользователь не найден.")


@swagger_path("app/views/user/swagger/save_user.yaml")
async def save_user(request):
    data = await request.json()

    try:
        validated_data = SaveNewUserSchema().load(data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    username = validated_data["username"]
    user_coordinates = Coordinates(x=validated_data["x"], y=validated_data["y"])

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:

        await save_user_validator(conn=conn, username=username, user_coordinates=user_coordinates)
        await save_user_query(conn=conn, username=username, user_coordinates=user_coordinates)

        return web.Response(status=201, text="Пользователь успешно создан.")


@swagger_path("app/views/user/swagger/delete_user.yaml")
async def delete_user(request):
    url_data = request.match_info

    try:
        validated_data = UserUrlParamsSchema().load(url_data)
    except ValidationError as err:
        return web.json_response(err.normalized_messages(), status=422)

    user_id = validated_data["user_id"]

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        await delete_user_validator(conn=conn, user_id=user_id)
        await delete_user_query(conn=conn, user_id=user_id)

    return web.Response(status=204)


@swagger_path("app/views/user/swagger/get_user_neighbors.yaml")
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

    user_id = validated_data["user_id"]
    radius = validated_data["radius"]
    limit = validated_data["limit"]

    async with request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
        user_coordinates_query = await get_user_coordinates(conn=conn, user_id=user_id)

        if user_coordinates_query:
            search_params = NeighborsSearchParameters(
                user_id=user_id,
                radius=radius,
                limit=limit,
                user_coordinates=Coordinates(
                    x=user_coordinates_query.x, y=user_coordinates_query.y
                ),
            )
            result = await get_user_neighbors_bl(
                conn=conn, search_parameters=search_params
            )
            json_data = json.dumps(result, ensure_ascii=False, cls=DecimalEncoder)

            return web.Response(body=json_data)

        else:
            return web.Response(status=404, text="Пользователь не найден.")
