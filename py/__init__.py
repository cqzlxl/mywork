##-*-coding: utf-8;-*-##
import functools


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