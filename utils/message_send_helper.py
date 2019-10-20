#!/usr/bin/env python
import logging

from utils import notice

logger = logging.getLogger("main")


def msg_sender(config, msg, docker_info):
    # 获取配置
    notice_config = config.get("notice")
    if not notice_config:
        logger.warn("未发现notice配置")
        return
    notice_method = notice_config.get("method")
    if not notice_method:
        logger.warn("未发现notice配置")
        return

    if not hasattr(notice, notice_method):
        logger.warn("notice方式不存在. 请检查配置")
        return
    timeout = notice_config.get("timeout", 10)
    msg_func = getattr(notice, notice_method)
    kwargs = {}
    if notice_method == "dingding":
        kwargs["timeout"] = timeout
        kwargs["token"] = notice_config["token"]
        kwargs["msg"] = msg
    elif notice_method == "webhook":
        docker_info["msg"] = msg

        kwargs["timeout"] = timeout
        kwargs["url"] = notice_config["url"]
        kwargs["hookinfo"] = docker_info
    else:
        logger.warn("notice方式不存在. 请检查配置")
        return
    msg_func(**kwargs)
