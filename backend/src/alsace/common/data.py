import flask
import logbook

import helpers
from ecutopia.generated.model import *


log = logbook.Logger(__name__)


def setting_query(is_deleted=False):
    T = Setting._table
    query = T.select(*Setting._columns, order_by=T.id)
    query.where = T.is_deleted == is_deleted
    sql, params = tuple(query)
    rows = helpers.db.execute(
        statement=sql, params=params, record_type=Setting).fetchall()
    return rows


def settings_load():
    local = getattr(flask.g, 'settings', None)
    if local is not None:
        return local

    from_cache = flask.current_app.cache.get('settings')
    if from_cache is not None:
        flask.g.settings = from_cache
        return from_cache

    rows = setting_query()
    flask.g.settings = result = {s.key: s.value for s in rows}
    flask.current_app.cache.set('settings', result, 30)
    return result
