#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import os
import scloud
import logging
import tornado.web
from tornado.options import options
from torweb.application import make_application 
from torweb.config import CONFIG
from torweb import run_torweb
from code import interact
from scloud.config import logger, settings_path, tornado_settings, CONF
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

logging.info("^_^")
logging.info(settings_path)

app = make_application(
    scloud,
    # debug=CONF("DEBUG_PAGE"),
    debug=False,
    wsgi=False,
    settings_path=settings_path,
    url_root=CONF("URL_ROOT"),
    **tornado_settings
)
from scloud.async_services.listener import init_listener
init_listener()
#setattr(app, '_wsgi', False)
if options.cmd == "runserver":
    import tcelery
    from scloud import celeryapp
    tcelery.setup_nonblocking_producer(celery_app=celeryapp.celery)
    run_torweb.run(app, port=CONF("PORT"))
elif options.cmd == "syncdb":
    logging.info("** start sycndb ... **")
    from scloud.models.user import User
    BaseModel.metadata.create_all(db_engine)
    logging.info("** end sycndb ... **")
else:
    run_torweb.show_urls(scloud)
