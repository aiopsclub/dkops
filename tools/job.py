#!/usr/bin/env python
import logging
import threading
import random

from tools.container_helper import container_handler
from utils.docker_helper import docker_client

logger = logging.getLogger("main")


def docker_monitor(config):
    logger.info("系统配置: {}".format(config))
    logger.info("docker version: {} ".format(docker_client.version().get("Version")))
    containers = docker_client.containers(size=True)
    if not containers:
        logger.info("Can't find any running container on this machine.")
    else:
        for item in containers:
            container_name = item.get("Names")[0]
            SizeRw = item.get("SizeRw", 0)
            SizeRootFs = item.get("SizeRootFs", 0)
            container_size_info = {
                "SizeRootFs": SizeRootFs,
                "SizeRw": SizeRw,
                "name": container_name,
            }
            docker_thread = threading.Thread(
                target=container_handler,
                daemon=True,
                args=(config, container_size_info),
                name="{}_container_thread_{}".format(
                    container_name.strip("/"), random.randint(0, 10000)
                ),
            )
            docker_thread.start()
