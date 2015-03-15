import helpers
from ecutopia.generated.model import Migration


def migration_query():
    T = Migration._table
    query = T.select(*Migration._columns, order_by=T.id)
    sql, params = tuple(query)
    rows = helpers.db.execute(statement=sql, params=params, record_type=Migration).fetchall()
    return rows
