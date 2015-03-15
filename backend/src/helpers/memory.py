import collections
import itertools
import sys


def recursive_sizeof(o, handlers={}, verbose=False, default_size=sys.getsizeof(0)):
    """Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses: tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    For objects without __sizeof__, `default_size` is used.

    From http://code.activestate.com/recipes/577504/
    """
    dict_handler = lambda d: itertools.chain.from_iterable(d.items())
    iteritems_handler = lambda d: itertools.chain.from_iterable(d.items())
    all_handlers = {
        tuple: iter,
        list: iter,
        collections.deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)  # user handlers take precedence
    seen = set()  # track which object id's have already been seen

    def sizeof(o):
        id_ = id(o)
        if id_ in seen:  # do not double count the same object
            return 0
        seen.add(id_)
        s = sys.getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o))

        handler = None
        for type_ in all_handlers:
            if isinstance(o, type_):
                handler = all_handlers[type_]
                break
        if handler is None and hasattr(o, 'iteritems'):
            handler = iteritems_handler
        if handler is not None:
            s += sum(map(sizeof, handler(o)))
        return s

    return sizeof(o)
