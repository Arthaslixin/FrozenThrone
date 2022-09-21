# coding=utf8
# @author: Arthas

import json
from component.log import logger
from config.config import SAVE_FILE_PATH



def save(index, data):
    raw_data = json.loads(SAVE_FILE_PATH)
    raw_data["data"][index] = data

def load():
    raw_data = json.loads(SAVE_FILE_PATH)
    index = raw_data["index"]
    return raw_data["data"][index]
