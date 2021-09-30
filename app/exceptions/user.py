from aiohttp.web_exceptions import HTTPNotFound, HTTPServerError


class UserDuplicateCoordinatesError(HTTPServerError):
    status = 500
    text = "Пользователь с такими координатами уже есть в базе."

    def __init__(self, text=text):
        super(UserDuplicateCoordinatesError, self).__init__(text=text)


class UserDuplicateNameError(HTTPServerError):
    status = 500
    text = "Пользователь с таким именем уже есть в базе."

    def __init__(self, text=text):
        super(UserDuplicateNameError, self).__init__(text=text)


class UserDoesNotExistError(HTTPNotFound):
    status = 500
    text = "Пользователя не существует."

    def __init__(self, text=text):
        super(UserDoesNotExistError, self).__init__(text=text)
