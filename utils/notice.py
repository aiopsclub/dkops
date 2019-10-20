#!/usr/bin/env python
import logging
import traceback

import requests

logger = logging.getLogger("main")


def dingding(token, msg, timeout=10):

    dingding_url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
    body = {"msgtype": "text", "text": {"content": msg}}
    try:
        dingding_res = requests.post(dingding_url, json=body, timeout=timeout)
        if dingding_res.json().get("errcode") != 0:
            logger.error(dingding_res.json().get("errmsg"))
        else:
            logger.info("钉钉消息发送成功")
        dingding_res.raise_for_status()
    except Exception:
        logger.error(traceback.format_exc())


def webhook(url, hookinfo, timeout=10):
    try:
        webhooks_res = requests.post(url, json=hookinfo, timeout=timeout)
        if webhooks_res.status_code == 200:
            logger.info("webhooks发送成功")
        else:
            logger.error("webhook消息发送失败")
    except Exception:
        logger.error("webhook消息发送失败")
        logger.error(traceback.format_exc())
