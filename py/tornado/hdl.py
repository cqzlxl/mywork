##-*-coding: utf-8;-*-##
import logging

import jsonpath_rw as jsonpath
import tornado.escape
from tornado.web import HTTPError
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def is_json_request(self):
        return self.request.headers.get('Content-Type', '').lower().startswith('application/json')


    def get_json_argument(self, path, default=None):
        for v in self._iter_json_arguments(path):
            return v
        else:
            return default


    def get_json_arguments(self, path):
        return [v for v in self._iter_json_arguments()]


    def not_found_error(self):
        raise HTTPError(404)


    def bad_request_error(self, reason=None):
        raise HTTPError(400, reason)


    def prepare(self):
        self._prepare_json_request()


    def _prepare_json_request(self):
        is_json = self.is_json_request()
        logging.debug('request is json? %s.', is_json)

        if not is_json:
            logging.debug('arguments: %s', self.request.arguments)
            self.request.json_arguments = dict()
            return

        try:
            self.request.json_arguments = tornado.escape.json_decode(self.request.body)
            logging.debug('arguments: %s', self.request.json_arguments)
        except Exception:
            logging.exception('wrong JSON request format: %s', self.request.body)
            self.bad_request_error('Wrong JSON reqeust Format')


    def _iter_json_arguments(self, path):
        for m in jsonpath.parse(path).find(self.request.json_arguments):
            yield m.value
