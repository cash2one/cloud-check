# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

import tornado.ioloop
import tornado.web
from scloud.config import logger


EXECUTOR = ThreadPoolExecutor(max_workers=4)


def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            if self._finished:
                logger.info("+++++++++++++++ future.result() +++++++++++++++")
                logger.info(future.result())
                return future.result()
            else:
                self.write(future.result())
                self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper
