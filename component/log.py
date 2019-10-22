# coding=utf8

import logging
import logging.config
import os
import yaml


def init_logger():
    """
    检查logs目录及log配置文件，读取log配置文件。
    """
    # 设置requests默认日志级别, 然而应该并用不到requests
    logging.getLogger("requests").setLevel(logging.WARNING)
    # 检查路径
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    log_config = yaml.load(open("./config/logging.yaml", "r"))
    logging.config.dictConfig(log_config)


logger = logging.getLogger("main")
