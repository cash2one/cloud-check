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
from scloud.config import CONF

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

