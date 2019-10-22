#!/usr/bin/env python
from typing import List
import socket
import os
import shutil


def common_method_choice(method: str):
    if method.startswith(("_", "__")):
        return False
    return True


def help_doc(property_list: List) -> List:
    return filter(common_method_choice, property_list)


def get_hostname():
    return socket.gethostname()


def calc_mem_precent(container_info):
    mem_info = container_info["memory_stats"]
    return (float(mem_info["usage"]) / mem_info["limit"]) * 100


def clean_lock_dir(config):
    lock_file_dir = config.get("lock_file_dir", "/var/run/dkops_locks/")
    if not os.path.exists(lock_file_dir):
        return
    else:
        shutil.rmtree(lock_file_dir, ignore_errors=True)


def ensure_lock_dir_exist(config):

    lock_file_dir = config.get("lock_file_dir", "/var/run/dkops_locks/")
    if not os.path.exists(lock_file_dir):
        os.makedirs(lock_file_dir)
    return lock_file_dir


def create_container_lock_file(config, container_name):
    lock_file_dir = ensure_lock_dir_exist(config, container_name)
    lock_file_name = os.path.join(lock_file_dir, container_name + ".lock")

    if not os.path.isfile(lock_file_name):
        fd = open(lock_file_name, mode="w", encoding="utf-8")
        fd.close()


def is_lock_file_exist(config, container_name):
    lock_file_dir = ensure_lock_dir_exist(config, container_name)
    return os.path.exists(os.path.join(lock_file_dir, container_name + ".lock"))
