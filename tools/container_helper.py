#!/usr/bin/env python
import logging


logger = logging.getLogger("main")


def container_handler(config, container_info):
    logger.info(config)
    logger.info(container_info)
