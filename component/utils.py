# coding=utf8
# @author: Arthas

import json
from component.log import logger


def make_response(err_code, **kwargs):
    """
    将参数转换为json格式的字符串作为响应。
    :param err_code:
    :param kwargs:
    :return:
    """

    response_body = json.dumps({"err_code": err_code, "content": kwargs})
    logger.info(f"response: {response_body}")
    return response_body
