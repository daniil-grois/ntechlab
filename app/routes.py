from aiohttp import web

from views.common.views import health_check
from views.user.views import save_user, delete_user, get_user, get_user_neighbors


routes = [
    web.get('/api/v1/user/{user_id}', get_user),
    web.get('/api/v1/get_user_neighbors/{user_id}', get_user_neighbors),
    web.post('/api/v1/save_user', save_user),
    web.delete('/api/v1/delete_user/{user_id}', delete_user),

    web.get('/api/v1/health_check', health_check)
]
