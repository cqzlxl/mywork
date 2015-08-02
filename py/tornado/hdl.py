##-*-coding: utf-8;-*-##
import logging

import tornado.escape
from tornado.web import HTTPError
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def is_json_request(self):
        return self.request.headers.get('Content-Type', '').lower() \
            == 'application/json'


    def prepare(self):
        self._prepare_json_request()


    def json_arg(self, name, default=None):
        return self.json_arguments.get(name, default)


    def _prepare_json_request(self):
        is_json = self.is_json_request()
        logging.debug('request is json? %s.', is_json)

        if not is_json:
            logging.debug('arguments: %s', self.request.arguments)
            self.json_arguments = dict()
            return

        try:
            self.json_arguments = tornado.escape.json_decode(self.request.body)
        except Exception:
            logging.exception('wrong JSON format: %s', self.request.body)
            raise HTTPError(400, 'Wrong JSON Format')
        else:
            logging.debug('arguments: %s', self.json_arguments)
