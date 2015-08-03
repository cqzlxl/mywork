##-*-coding: utf-8;-*-##
from abc import ABCMeta


def interface(*attributes):
    '''Usage:
    @interface('x', 'y', 'z')
    class Interface(object):
        __metaclass__ = abc.ABCMeta
    '''

    def decorator(Class):
        @classmethod
        def __subclasshook__(cls, c):
            if cls is not Class:
                return NotImplemented

            names = list()
            for b in c.__mro__:
                names.extend(b.__dict__.keys())

            if set(attributes) <= set(names):
                return True
            else:
                return NotImplemented

        Class.__subclasshook__ = __subclasshook__
        return Class

    return decorator
