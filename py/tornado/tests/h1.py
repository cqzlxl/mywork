##-*-coding: utf-8;-*-##
import logging

import hdl
import req
import url

@url.mapping(r'/')
class RootHandler(hdl.BaseHandler):

    @req.hosts_only()
    def get(self):
        logging.debug('%s', self.request)
        self.write('Welcome!')


    def head(self):
        pass
