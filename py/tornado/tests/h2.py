##-*-coding: utf-8;-*-##
import hdl
import url


@url.mapping('/hello')
class HelloHandler(hdl.BaseHandler):
    def get(self):
        self.write('Hello, {}!'.format(self.get_argument('name', 'world')))
