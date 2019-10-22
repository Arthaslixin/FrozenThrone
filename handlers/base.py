# coding=utf8
# @author: Arthas

import tornado.web
import json
from config.config import StatusCode
import urllib.parse
from component.log import logger
from component.utils import make_response


class BaseHandler(tornado.web.RequestHandler):
    """
    Handler父类，定义一些公共方法
    """
    SUBCLS = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        url_key = cls.__name__[:-7]
        if url_key not in cls.SUBCLS:
            cls.SUBCLS[url_key] = cls

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.response = None

    @classmethod
    def get_sub_cls(cls):
        return cls.SUBCLS

    def parse_json(self):
        """
        将解析请求体中的json格式字符串或form-data解析成字典并更新为self.json

        Returns:
            True or ERROR
        """

        def _parse_form_and_urlencode(self, arguments):
            _json = {}
            for k, v in arguments.items():
                value = v[0].decode("utf8")
                try:
                    if "_" not in value:
                        value = int(value)
                except Exception:
                    pass
                _json[k] = value
            self.json = _json
            return True

        if self.request.method == "GET" and self.request.query_arguments:
            if _parse_form_and_urlencode(self, self.request.query_arguments):
                return True
            else:
                return make_response(StatusCode.invalid_params)
        elif self.request.method == "POST" and self.request.body:
            pattern = 'Content-Disposition: form-data; name="(\w+)"("?\w+"?)----------------------------'
            try:
                body = (
                    self.request.body.decode("utf8")
                        .replace("\n", "")
                        .replace("\r", "")
                )
            except Exception:
                if not _parse_form_and_urlencode(self, self.request.arguments):
                    logger.info(traceback.print_exc())
                    return make_response(err.ERR_INVALID_PARAMS)
                return True
            from_data_idx = re.findall(pattern, body)
            if from_data_idx:
                if not _parse_form_and_urlencode(self, self.request.arguments):
                    return make_response(err.ERR_INVALID_PARAMS)
            else:
                try:
                    json_ = json.loads(body)
                    self.json = json_
                    return True
                except Exception:
                    logger.exception("直接loads body出错，尝试按照查询串解析")

                try:
                    # 最后再救一次
                    body = urllib.parse.unquote(body)
                    body_params_list = urllib.parse.parse_qsl(body)
                    temp_params_dict = dict()
                    for item in body_params_list:
                        temp_params_dict.update({item[0]: item[1]})
                    if len(temp_params_dict) > 0:
                        self.json = temp_params_dict
                except:
                    logger.info("尝试按照查询串解析body出错")
                    return make_response(StatusCode.invalid_params, body=body)
        return True

    def get_custom_header(self):
        """
        若需要自定义header在此处设置
        Returns:

        """
        return None

