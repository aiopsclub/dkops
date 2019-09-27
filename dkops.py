#!/usr/bin/env python
import os
import re
import sys

import fire
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler

from utils.config import Config
from utils.helper import help_doc
from utils.logger import Logger


class DkOps(object):
    def __init__(self, config_file="./dkops.yaml"):
        self._version = "0.0.1"
        self.config_file = config_file
        self.config = {}

    @property
    def version(self):
        return self._version

    @classmethod
    def usage(cls):
        usage_list = ["{} Usage:".format(sys.argv[0])]
        usage_list.extend(
            [("    {} {}".format(sys.argv[0], item)) for item in help_doc(dir(cls))]
        )
        print("\n".join(usage_list))

    def __str__(self):
        return self.version

    def __loadconfig(self):
        if not os.path.exists(self.config_file):
            print("config file {} not found!! exit...")
            sys.exit(1)
        self.config = Config(self.config_file).analysis()

    def __initlogger(self):
        log_file = self.config["common"].get("log_file", "./log/dkops.log")
        log_level = self.config["common"].get("log_level", "error")
        self.logger = Logger(log_file, level=log_level).logger

    def start(self):
        self.__loadconfig()
        self.__initlogger()
        self.logger.info("Start... version: {}".format(self.version))


def main():
    help_pattern = re.compile("(-h|--help)")
    if len(sys.argv) == 2 and help_pattern.match(sys.argv[1]):
        DkOps.usage()
        sys.exit(0)
    else:
        fire.Fire(DkOps)


if __name__ == "__main__":
    main()
