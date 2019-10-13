#!/usr/bin/env python
import logging

import docker

logger = logging.getLogger("main")


def docker_monitor():
    docker_client = docker.APIClient(base_url="unix://var/run/docker.sock")
    logger.info("docker version: {} ".format(docker_client.version().get("Version")))
    containers = docker_client.containers(size=True)
    if not containers:
        logger.info("未发现任何运行的容器")
    else:
        for item in containers:
            container_name = item.get("Names")[0]
            logger.info(docker_client.stats(container_name, stream=False))
