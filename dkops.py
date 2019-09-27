#!/usr/bin/env python

import os
import sys

import fire

from utils.config import Config
from utils.logger import Logger


class DkOps(object):
    def __init__(self, config_file="./dkops.yaml"):
        self._version = "0.0.1"
        self.config_file = config_file
        self.config = {}

    def version(self):
        return self._version

    def __loadconfig(self):
        if not os.path.exists(self.config_file):
            print("config file {} not found!! exit...")
            sys.exit(1)
        self.config = Config(self.config_file).analysis()

    def __initlogger(self):
        log_file = self.config["common"].get("log_file", "./log/dkops.log")
        log_level = self.config["common"].get("log_level", "error")
        self.logger = Logger(log_file, level=log_level)

    def start(self):
        pass


if __name__ == "__main__":
    fire.Fire(DkOps)
