#!/usr/bin/env python

import docker

docker_client = docker.APIClient(base_url="unix://var/run/docker.sock")
