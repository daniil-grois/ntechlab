from aiopg.sa.result import RowProxy
from sqlalchemy.sql.schema import Table


def simple_sqlalchemy_core_serializer(data: RowProxy, table: Table):
    return {c.name: getattr(data, c.name) for c in table.columns}
