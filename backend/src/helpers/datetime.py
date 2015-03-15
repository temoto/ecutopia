import datetime


def datetime_to_tuple(dt, precision=None):
    """datetime, precision -> tuple(year, month, day, hour, minute, second, microsecond)[:precision]

    Reverse operation is `datetime(*tuple)`.
    """
    full = (dt.year, dt.month, dt.day, dt.hour,
            dt.minute, dt.second, dt.microsecond)
    return full[:precision] if precision else full


def datetime_to_unix(dt, _epoch_ord=datetime.date(1970, 1, 1).toordinal()):
    """UTC datetime -> UNIX timestamp

    Invariant: `datetime.utcfromtimestamp(datetime_to_unix(dt)) == dt`
    """
    days = dt.date().toordinal() - _epoch_ord
    hours = days * 24 + dt.hour
    minutes = hours * 60 + dt.minute
    seconds = minutes * 60 + dt.second
    return seconds + dt.microsecond / 1e6


def str_to_date(s, format="%Y-%m-%d", _parse=datetime.datetime.strptime):
    """ '2012-11-13' -> date(2012, 11, 13)
    """
    dt = _parse(s, format)
    return dt.date()
