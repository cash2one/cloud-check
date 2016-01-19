#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import sys
from os.path import abspath, dirname, join
base_path = abspath(dirname(__file__))

# 添加系统路径
import sys
sys.path.insert(0, abspath(join(base_path, '..')))
import os
from celery import Celery
from code import interact

os.environ.setdefault("CELERY_CONFIG_MODULE", "scloud.celeryconfig")

celery = Celery()
celery.config_from_envvar('CELERY_CONFIG_MODULE')
#interact(local=locals())
#celery.config_from_object(celeryconfig)

#import kombu.serialization
#kombu.serialization.enable_insecure_serializers(choices=['json'])
# kombu.serialization.registry.enable('application/x-python-serialize')


if __name__ == '__main__':
    celery.start()
