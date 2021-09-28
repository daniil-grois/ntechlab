from aiohttp import web

from views import UserView


routes = [
    web.get('/api/user/{user_id}', handler=UserView),
    web.view('/api/user', UserView),
    web.delete('/api/user/{user_id}', handler=UserView),
]
