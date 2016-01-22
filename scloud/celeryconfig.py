#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from celery.schedules import crontab

BROKER_URL = "amqp://"
CELERY_RESULT_BACKEND = "amqp"
# CELERY_RESULT_BACKEND = "redis"
#BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 18000}

CELERY_EVENT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']  # ['pickle', 'json', 'msgpack', 'yaml']

CELERYD_CONCURRENCY = 5

CELERYD_TASK_TIME_LIMIT = 60 * 10   # resolve celery does not release memory

CELERYD_OPTS = "--time-limit=7200 -E --loglevel=INFO"
# try resolve TimeLimitExceeded: TimeLimitExceeded

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_IMPORTS = (
    # 'scloud.tasks',
    'scloud.async_services.svc_act',
    'scloud.async_services.svc_project',
    'scloud.async_services.svc_pt_permission',
)
