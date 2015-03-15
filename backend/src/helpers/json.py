import decimal
import json


def default(x, _Decimal=decimal.Decimal):
    if isinstance(x, _Decimal):
        return str(x)
    raise TypeError


dumps = lambda *a, **kw: json.dumps(*a, default=default, **kw)
loads = json.loads
