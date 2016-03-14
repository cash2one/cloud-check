# -*- coding: utf-8 -*-

import os
import yaml
import uuid
import base64
import logging
import scloud
import traceback
from functools import wraps
from tornado.util import ObjectDict
from torweb.config import get_host_ip, CONFIG
from torweb.urls import Url
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler
from scloud.utils.error_code import ERROR


CONFIG_NAME = "prd.yaml"
host_ip = get_host_ip()


import uuid
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

host_mac = get_mac_address()

def get_config_name():
    config_choices = {
        '192.168.1.108': 'dev.yaml',
        '20:68:9d:48:a9:40': 'dev.yaml',
    }
    return config_choices.get(host_ip, None) or config_choices.get(host_mac, None) or CONFIG_NAME

settings_path = os.path.join(scloud.base_path, "settings", get_config_name())
dictConfig(yaml.load(open(settings_path, 'r')))
itornado = logging.getLogger("console")
logger = logging.getLogger("file")
iError = logging.getLogger("iError")
CONF = CONFIG(settings_path)


def logThrown():
    logger.critical(traceback.format_exc())
    logger.critical('-'*60)


def thrownException(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(args)
            logger.info(kwargs)
            logger.info("====[EXIT]====")
            # svc = args[0]
            # # from code import interact
            # # interact(local=locals())
            # if isinstance(e, Exception):
            #     svc.db.rollback()
            #     logger.info("====[ROLLBACK]====")
            # else:
            #     svc.db.commit()
            #     # svc.db.flush()
            #     logger.info("====[COMMIT]====")
            # svc.db.remove()
            # svc.db.close()
            logger.info("====[CLOSE]====")
            # svc = args[0]
            # svc.db.close()
            # svc.db.remove()
            # logger.info(svc.db)
            logThrown()
            data = ObjectDict()
            data.return_code = ERROR.system_err.errcode
            data.return_message = e.__unicode__()
            return data
    return wrapper

static_path = os.path.join(scloud.base_path, "static")
logger.info("static_path: %s" % static_path)
tornado_settings = {
    "static_path": static_path,
    "static_url_prefix": "%s/static/" % CONF("URL_ROOT"),
    'cookie_secret': base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    'xsrf_cookies': True,
}
logger.info("tornado_settings: %s" % tornado_settings)


# url = Url(CONF("URL_ROOT"))

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
