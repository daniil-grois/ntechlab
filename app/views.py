from aiohttp import web

from config import settings
from services.db.models import UserTable
from services.db.queries import get_user_coordinates, save_user, delete_user, get_users_inside_square


class UserView(web.View):
    async def get(self):
        user_id = self.request.match_info['user_id']

        radius = float(self.request.rel_url.query['radius'])
        limit = int(self.request.rel_url.query['limit'])

        async with self.request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
            user_x, user_y = await get_user_coordinates(conn=conn, user_id=user_id)

            users = await get_users_inside_square(
                conn, user_id=user_id, x=user_x, y=user_y, radius=radius, limit=limit)

            all_users_in_circle = tuple(filter(lambda user: user.hypotenuse <= radius, users))
            all_sorted_users_in_circle = sorted(all_users_in_circle, key=lambda user: user.hypotenuse)

            response_data = []
            for i in all_sorted_users_in_circle:
                response_data.append({c.name: getattr(i, c.name) for c in UserTable.columns})

        return web.json_response(response_data)

    async def post(self):
        data = await self.request.json()

        username = data['username']
        x = data['x']
        y = data['y']

        async with self.request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
            await save_user(conn=conn, username=username, x=x, y=y)

        return web.Response(status=201, text="Пользователь успешно создан.")

    async def delete(self):
        user_id = self.request.match_info['user_id']

        async with self.request.app[settings.DB_CONFIG.DB_ENGINE_CONSTANT].acquire() as conn:
            await delete_user(conn=conn, user_id=user_id)

        return web.Response(status=204, text="Пользователь успешно удален.")
