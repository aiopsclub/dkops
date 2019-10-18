#!/usr/bin/env python
from typing import List


def common_method_choice(method: str):
    if method.startswith(("_", "__")):
        return False
    return True


def help_doc(property_list: List) -> List:
    return filter(common_method_choice, property_list)


def get_hostname():
    return socket.gethostname()
