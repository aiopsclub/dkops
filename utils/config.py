#!/usr/bin/env python
import yaml


class Config(object):
    def __init__(self, config_file):
        # config_file must abs path
        self.config_file = config_file

    def analysis(self):
        with open(self.config_file) as fd:
            return yaml.load(fd, Loader=yaml.FullLoader)
