##-*-coding: utf-8;-*-##
import contextlib
import functools
import sys
import time


def catch_type_error_in_op(special):
    @functools.wraps(special)
    def wrapper(*args, **kargs):
        try:
            return special(*args, **kargs)
        except TypeError:
            return NotImplemented

    return wrapper


def coroutine(func):
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        gen = func(*args, **kargs)
        next(gen)
        return gen

    return wrapper


@contextlib.contextmanager
def timed_scope(label=None):
    t0 = time.time()
    prefix = u'timed scope [{}]'.format('' if label is None else label)
    print >>sys.stderr, prefix, u'started'
    try:
        yield
    except Exception:
        raise
    finally:
        t1 = time.time()
        print >>sys.stderr, prefix, u'finished'
        print >>sys.stderr, prefix, t1-t0, 'seconds used'
