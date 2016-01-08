##-*-coding: utf-8;-*-##
import inspect
import logging

from tornado.web import RequestHandler
from tornado.web import URLSpec


SUPPORTED_METHODS = set((
    'get',
    'post',
    'put',
    'head'
))


urlspecs = dict()


def mapping(pattern, args=None, name=None):
    def wrapper(class_):
        assert issubclass(class_, RequestHandler)

        supported = set()
        for k,v in class_.__dict__.items():
            if k in SUPPORTED_METHODS and inspect.isfunction(v):
                supported.add(k)

        urlspecs[pattern] = URLSpec(pattern, class_, args, name)

        logging.debug('URL mapping: %s ==> %s', pattern, class_.__name__)
        logging.debug('URL mapping: name = %s', name)
        logging.debug('URL mapping: args = %s', args)
        logging.debug('URL mapping: methods = %s', list(supported))
        return class_

    return wrapper


def load_mappings(loader):
    loader()
    return urlspecs.values()
