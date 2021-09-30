from aiopg.sa.result import RowProxy
from sqlalchemy.sql.schema import Table


def simple_sqlalchemy_core_serializer(data: RowProxy, table: Table):
    """На скорую руку сделанный сериалайзер. Вместо него на выходе
    все обрабатывать должна marshmallow schema dump. Не успел :/"""
    return {c.name: getattr(data, c.name) for c in table.columns}
