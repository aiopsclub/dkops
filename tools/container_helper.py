#!/usr/bin/env python
from utils.helper import calc_mem_precent
from utils.docker_helper import docker_client
import logging
import sys


logger = logging.getLogger("main")


def container_handler(config, container_info):
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
            logger.warn(
                "container {} memory over limit. restart it".format(container_name)
            )
            docker_client.restart(
                container_info["id"], config["common"]["restart_timeout"]
            )
        else:
            logger.info("container {} memory is normal.".format(container_name))
    else:
        logger.info(
            "container {} limit conifg not found, skip...".format(container_name)
        )
