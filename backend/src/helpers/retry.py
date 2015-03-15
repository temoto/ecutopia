import functools
# import logging
import time

import logbook


log = logbook.Logger(__name__)
# log = logging.getLogger(__name__)


def repr_func(f):
    """Attempt to get the most useful string representation of callable.
    """
    name = getattr(f, 'func_name', '<unknown>')
    func_code = getattr(f, 'func_code', None)
    if func_code is not None:
        return u'{name}() @ {fc.co_filename}:{fc.co_firstlineno}'.format(
            name=name,
            fc=func_code)

    return repr(f)


def retry(tries, exceptions=(Exception,), delay=0):
    """
    Decorator for retrying a function if exception occurs

    tries -- num tries
    exceptions -- exceptions to catch
    delay -- wait between retries
    """
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            n = tries  # copy to local variable for modification
            while n > 0:
                n -= 1
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if n == 0:
                        raise
                    # logbook
                    # log.error(u'retry: {f} {e}', f=repr_func(func), e=e)
                    # logging
                    log.error(u'retry: %s %s', repr_func(func), e)
                    time.sleep(delay)
        return wrapped
    return wrapper
