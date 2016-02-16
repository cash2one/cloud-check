# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

import tornado.ioloop
import tornado.web
from scloud.config import logger
from scloud.utils.error import SystemError


EXECUTOR = ThreadPoolExecutor(max_workers=4)


def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            try:
                if self._finished:
                    logger.info("+++++++++++++++ future.result() +++++++++++++++")
                    logger.info(future.result())
                    return future.result()
                else:
                    self.write(future.result())
                    self.finish()
            except Exception as e:
                if isinstance(e, SystemError):
                    template_string = self.render_to_string("admin/error/500.html", status_code=500, exception=u"系统错误(%s)" % e.code, traceback=e.message)
                    self.write(template_string)
                    self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper
