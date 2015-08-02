##-*-coding: utf-8;-*-##
import functools
import logging

from tornado.web import HTTPError


def json_only(method):
    @functools.wraps(method)
    def wrapper(self, *vargs, **kargs):
        if self.is_json_request():
            return method(self, *vargs, **kargs)

        logging.error('request content type should be JSON')
        raise HTTPError(400, 'JSON Request Only')

    return wrapper


def hosts_only(hosts=['127.0.0.1']):
    '''针对一系列相关的路径做限制时，最好还是采用Nginx来实现。'''

    def decorator(method):
        limited = set(hosts)

        @functools.wraps(method)
        def wrapper(self, *vargs, **kargs):
            if self.request.remote_ip in limited:
                return method(self, *vargs, **kargs)

            logging.error('client IP not allowed: %s', self.request.remote_ip)
            logging.error('client IP allowed by admin: %s', list(limited))
            raise HTTPError(403, 'Clinet IP Not Allowed')

        return wrapper

    return decorator
