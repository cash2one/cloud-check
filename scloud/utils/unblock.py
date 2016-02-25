# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

import simplejson
import tornado.ioloop
import tornado.web
from scloud.config import logger, logThrown
from scloud.utils.error import SystemError, NotFoundError
from scloud.utils.error_code import ERROR


EXECUTOR = ThreadPoolExecutor(max_workers=4)


def return_future(handler, ):
    if self._finished:
        logger.info("+++++++++++++++ future.result() +++++++++++++++")
        logger.info(future.result())
        return future.result()
    else:
        # logger.info("+++++++++++++++ future.result() +++++++++++++++")
        # logger.info(future.result())
        self.write(future.result())
        self.finish()

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
                    # logger.info("+++++++++++++++ future.result() +++++++++++++++")
                    # logger.info(future.result())
                    self.write(future.result())
            except Exception as e:
                logThrown()
                if isinstance(e, SystemError):
                    template_string = self.render_to_string("admin/error/500.html", status_code=500, exception=u"系统错误(%s)" % e.code, traceback=e.message)
                    if self.ajax:
                        self.write(simplejson.dumps(self.failure(e.code, e.message)))
                    else:
                        self.write(template_string)
                if isinstance(e, NotFoundError):
                    template_string = self.render_to_string("admin/error/404.html", status_code=404, exception=u"数据查询异常(%s)" % e.code, traceback=e.message)
                    if self.ajax:
                        self.write(simplejson.dumps(self.failure(e.code, e.message)))
                    else:
                        self.write(template_string)
                else:
                    template_string = self.render_to_string("admin/error/500.html", status_code=500, exception=u"系统错误", traceback=e.__unicode__())
                    if self.ajax:
                        self.write(simplejson.dumps(self.failure(ERROR.system_err.errcode, "(%s)%s:%s" % (ERROR.system_err.errcode, ERROR.system_err.errvalue, e.__unicode__()))))
                    else:
                        self.write(template_string)

            self.finish()
        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper
