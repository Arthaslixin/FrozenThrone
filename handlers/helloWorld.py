# coding=utf8
# @author: Arthas

from handlers.base import BaseHandler
from component.utils import make_response
from config.config import StatusCode


class HelloWorldHandler(BaseHandler):
    async def hello_world(self):
        arg = self.json.get("arg")
        return make_response(StatusCode.success, arg=arg)
