from aiohttp.web_exceptions import HTTPServerError


class ServerError(HTTPServerError):
    status = 500
    text = "Внутренняя ошибка сервера."

    def __init__(self, text=text):
        super(ServerError, self).__init__(text=text)
