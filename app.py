#!/usr/bin/env python3
# coding=utf8
# @author: Arthas

import tornado.ioloop
import tornado.web
from handlers.main import MainHandler
from tornado.options import define, options
from handlers.main import find_handler
from tornado.httpserver import HTTPServer
from component.log import init_logger
import tornado.autoreload
import os

define("port", default=8888, help="run on the given port", type=int)
define("address", default="0.0.0.0", help="run on the given address", type=int)
define("HANDLER_ROUTE", default=find_handler(), type=dict)

class FrozenThrone(tornado.web.Application):
    debug = True

    def __init__(self, command_options):
        self.options = command_options
        handlers = self.get_handlers()
        init_logger()
        super().__init__(
            handlers,
            debug=self.debug,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            static_url_prefix="/static/",
        )

    def get_handlers(self):
        return [
            ("^/.*\/?.*", MainHandler),
        ]


if __name__ == "__main__":
    http_server = HTTPServer(FrozenThrone(options), xheaders=True)
    http_server.listen(options.port, options.address)
    tornado.ioloop.IOLoop.current().start()
