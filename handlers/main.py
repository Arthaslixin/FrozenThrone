# coding=utf8

from component.log import logger
import tornado.web
import importlib
from handlers.base import BaseHandler
import os
import time

class MainHandler(tornado.web.RequestHandler):
    """
    项目的统一入口，解析url并调用对应的Handler中的对应的接口
    """

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Methods", "HEAD, OPTIONS, GET, POST, DELETE, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")

    async def route(self):
        """
        所有接口调用走这个函数处理
        :return:
        """
        url_dict = self.application.options.HANDLER_ROUTE
        logger.info(f"url: {self.request.uri}")
        # 截取uri 以便对应所访问的接口
        url_group = self.request.uri.split("/")
        if len(url_group) < 3:
            start = 1587484800
            delta = int((time.time() - start) // 86400 + 1)
            return f"爱你~ 我们在一起{delta}天啦"
        handler_name = url_group[1].lower()
        interface_name = url_group[2].lower()
        if interface_name.find("?") != -1:
            interface_name = interface_name[: interface_name.find("?")]
        if not url_dict.get(handler_name):
            return 404
        handler = url_dict[handler_name](self.application, self.request)
        if not hasattr(handler, interface_name):
            return 404
        # 解析函数
        parse_json_res = handler.parse_json()
        if parse_json_res is not True:
            return parse_json_res
        # if not hasattr(handler, "json"):
        #     return "json都没有你来请求啥"
        # logger.info(f"request {handler_name}/{interface_name}, params:{handler.json}")

        res = await getattr(handler, interface_name)()

        custom_header = handler.get_custom_header()
        if custom_header:
            for key, value in custom_header.items():
                self.set_header(key, value)
        return res

    async def get(self):
        res = await self.route()
        if res == 404:
            self.write_error(404)
        else:
            self.write(res)

    async def head(self):
        pass

    def options(self):
        pass

    async def post(self):
        res = await self.route()
        if res == 404:
            self.write_error(404)
        else:
            self.write(res)


def find_handler():
    """
    Returns:
        result: 收集到的各个handler的路由表
    """
    module_list = os.listdir("handlers")
    cls_require_imp = []
    for module_item in module_list:
        try:
            module = importlib.import_module(f"handlers.{module_item.split('.')[0]}")
            for cls in filter(lambda x: x.endswith("Handler"), dir(module)):
                obj = getattr(module, cls)
                if cls == "BaseHandler":
                    continue
                if issubclass(obj, BaseHandler):
                    cls_require_imp.append(cls)
                else:
                    continue
        except Exception:
            import traceback
            print(traceback.format_exc())
            pass
    url_dict = BaseHandler.get_sub_cls()
    result = {}
    for k, v in url_dict.items():
        result[k.lower()] = v
    return result
