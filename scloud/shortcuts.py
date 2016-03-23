#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import scloud
import os
import yaml
import logging
from logging.config import dictConfig
import traceback

from torweb.urls import Url
from torweb.tmpl import get_environment
from scloud.config import CONF, logger
from scloud.utils.error_code import ERROR as ERR
from tornado.web import Application
# from torweb.application import reverse_url
# from torweb.application import make_application

env = get_environment(scloud.__name__)
from scloud.utils.filters import Filters
Filters.init(env)

url = Url(CONF("URL_ROOT"))

# cache = scloud.cache
def get_cache():
    from torweb.cache import MemcachedCache, NullCache
    from werkzeug.contrib.cache import RedisCache
    nullcache = NullCache()
    try:
        cache_servers = CONF('MEMCACHED')
        if cache_servers:
            cache = MemcachedCache(cache_servers)
    except KeyError:
        redis_cache_host = CONF("REDIS.HOST")
        redis_cache_port = CONF("REDIS.PORT")
        if redis_cache_host and redis_cache_port:
            cache = RedisCache(redis_cache_host, redis_cache_port)
    except KeyError:
        cache = NullCache()
    return cache

cache = get_cache()

# from torweb.urls import url_rules, except_url, url404
# def _set_debug(kw):
#     kw["debug"] = debug
#     return kw
# url_handlers = []
# # url_rules.extend(url404.handlers)
# # app_url_handlers = url_rules
# url_handlers.extend(url_rules)
# # url_handlers.extend(except_url.handlers)
# url_handlers = [URLSpec(spec.regex.pattern, spec.handler_class, _set_debug(spec.kwargs), spec.name) for spec in url_handlers]
# 
# logger.info(url_handlers)
# 
# application = make_application(scloud)

def render_to_string(tmpl, **kwargs):
    from scloud.app import reverse_url
    template = env.get_template(tmpl)
    kwargs.update({
        "CONF": CONF,
        "reverse_url": reverse_url,
        "ERR": ERR,
    })
    template_string = template.render(**kwargs)
    return template_string
