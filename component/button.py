# coding=utf8
# @author: Arthas

import json
from component.log import logger

def get_button(data):
    """
        data = [{text: "", args: {}}]
    """
    res = f"""<div>"""
    for each_button in data:
        if len(each_button["args"]) > 0:
            url = "game" + "?"
            for k, v in each_button["args"].items():
                url += k + "=" + v + "&"
        res += f"""<span><button style="width:100px;height:60px;font-size:250%" onclick="location='{url}'">{each_button["text"]}</button></span>""" 
    res += f"""</div>"""
    return res