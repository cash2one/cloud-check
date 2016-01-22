#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>


# 添加系统路径
import sys
import os
from os.path import abspath, dirname, join
from celery import Celery

base_path = abspath(dirname(__file__))
sys.path.insert(0, abspath(join(base_path, '..')))

os.environ.setdefault("CELERY_CONFIG_MODULE", "scloud.celeryconfig")

celery = Celery()
celery.config_from_envvar('CELERY_CONFIG_MODULE')
