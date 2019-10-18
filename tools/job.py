#!/usr/bin/env python
import logging
from tools.container_helper import container_handler
from utils.docker_helper import docker_client

logger = logging.getLogger("main")


def docker_monitor(config):
    logger.info(config)
    logger.info("docker version: {} ".format(docker_client.version().get("Version")))
    containers = docker_client.containers(size=True)
    if not containers:
        logger.info("Can't find any running container on this machine.")
    else:
        for item in containers:
            container_name = item.get("Names")[0]
            SizeRw = item.get("SizeRw", 0)
            SizeRootFs = item.get("SizeRootFs", 0)
            docker_stats = docker_client.stats(container_name, stream=False)
            docker_stats["SizeRw"] = SizeRw
            docker_stats["SizeRootFs"] = SizeRootFs
            container_handler(config, docker_stats)
