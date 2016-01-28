#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.async_services.listener import init_listener
from scloud.celeryapp import celery


if __name__ == "__main__":
    init_listener()
    celery.start()
