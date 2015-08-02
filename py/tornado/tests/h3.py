##-*-coding: utf-8;-*-##
import logging

import hdl
import req
import url


@url.mapping('/logging')
class LoggingHandler(hdl.BaseHandler):
    @req.hosts_only(['192.168.1.103'])
    @req.json_only
    def post(self):
        if self.json_arg('debug', False):
            logging.getLogger().setLevel(logging.DEBUG)
            logging.info('online debug logging enabled')
        else:
            logging.getLogger().setLevel(logging.INFO)
            logging.info('online debug logging disabled')
