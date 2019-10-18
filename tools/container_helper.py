#!/usr/bin/env python
import logging
import sys


logger = logging.getLogger("main")


def container_handler(config, container_info):
    container_name = container_info.get("name", "").strip("/")
    if container_name in config.get("container_limit"):
        limit_config = config["container_limit"][container_name]
        # 判断limit_confi的具体配置
        if limit_config == "default":
            mem_limit = config.get("default_limit", {}).get("memory", 20)
        elif isinstance(limit_config, dict):
            mem_limit = limit_config.get("memory", 20)
        else:
            logger.warn("container {} limit config can't discriminate. skip it..")
            sys.exit(1)
        logger.info(mem_limit)

    else:
        logger.info(
            "container {} limit conifg not found, skip...".format(container_name)
        )


def calc_mem_precent(container_info):
    mem_info = container_info["memory_stats"]
    return (float(mem_info["usage"]) / mem_info["limit"]) * 100
