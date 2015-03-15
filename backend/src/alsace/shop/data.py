import helpers
from ecutopia.generated.model import *


def product_query(is_active=True, is_deleted=False):
    T = Product._table
    query = T.select(*Product._columns, order_by=T.id)
    query.where = (
        T.is_active == is_active
        and T.is_deleted == is_deleted
    )
    sql, params = tuple(query)
    rows = helpers.db.execute(statement=sql, params=params, record_type=Product).fetchall()
    return rows
