#!/usr/bin/env python
import logging
import sys
import traceback

from utils.docker_helper import docker_client
from utils.helper import calc_mem_precent
from utils.message_send_helper import msg_sender


logger = logging.getLogger("main")


def container_handler(config, container_size_info):
    container_info = docker_client.stats(container_size_info["name"], stream=False)
    container_info["SizeRw"] = container_size_info["SizeRw"]
    container_info["SizeRootFs"] = container_size_info["SizeRootFs"]
    container_name = container_info.get("name", "").strip("/")
    if container_name in config.get("container_limit"):
        limit_config = config["container_limit"][container_name]
        # 判断limit_config的具体配置
        if limit_config == "default":
            mem_limit = config.get("default_limit", {}).get("memory", 20)
        elif isinstance(limit_config, dict):
            mem_limit = limit_config.get("memory", 20)
        else:
            logger.warn("container {} limit config can't discriminate. skip it..")
            sys.exit(0)
        logger.info("container {} memory limit {}%".format(container_name, mem_limit))
        if calc_mem_precent(container_info) >= mem_limit:
            first_msg = "container {} memory over limit. restart it".format(
                container_name
            )
            logger.warn(first_msg)
            msg_sender(config, first_msg, container_info)
            try:
                docker_client.restart(
                    container_info["id"],
                    config.get("common", {}).get("restart_timeout", 600),
                )
            except Exception:
                logging.error(traceback.format_exc())
                end_msg = "container {} restart failed!".format(container_name)
            else:
                end_msg = "container {} restart successfully!".format(container_name)
            logger.warn(end_msg)
            msg_sender(config, end_msg, container_info)
        else:
            logger.info("container {} memory is normal.".format(container_name))
    else:
        logger.info(
            "container {} limit conifg not found, skip...".format(container_name)
        )
