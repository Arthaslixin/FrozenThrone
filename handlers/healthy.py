# coding=utf8
# @author: Arthas

from handlers.base import BaseHandler
from component.utils import make_response
from config.config import StatusCode
from component.button import *
import traceback


class HealthyHandler(BaseHandler):
    async def get_user(self):
        try:
            res = ""
            arg = self.json.get("arg")
            if not arg:
                pass
            else:
                res += get_button([{"text": str(each), "args": {"arg": str(each + 1)}} for each in range(1, arg+1)])
        except:
            print(traceback.format_exc())
        return res