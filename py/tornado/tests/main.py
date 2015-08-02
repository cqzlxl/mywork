##-*-coding: utf-8;-*-##
assert __name__ == '__main__'


import logging
import sys

import tornado.ioloop
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

import url


define('host',  '127.0.0.1', help='server listening host', type=str)
define('port',  8888,        help='server listening port', type=int)
define('debug', True,        help='start server in debug mode', type=bool)

def load_handlers():
    import tests.h1
    import tests.h2
    import tests.h3

application = tornado.web.Application(
    url.load_mappings(load_handlers),
    debug=options.debug
)

parse_command_line(sys.argv)
logging.basicConfig(level=logging.DEBUG)

application.listen(options.port, options.host)
logging.info(
    'server is listening at %s:%d, debug mode enabled: %s',
    options.host,
    options.port,
    options.debug
)

tornado.ioloop.IOLoop.current().start()
