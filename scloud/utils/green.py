# -*- coding: utf-8 -*-

import sys
import time
import greenlet
from tornado.ioloop import IOLoop
from tornado.concurrent import Future


class GreenTask(greenlet.greenlet):
    def __init__(self, run, *args, **kwargs):
        super(GreenTask, self).__init__()
        self._run = run
        self._args = args
        self._kwargs = kwargs
        self._future = Future()
        self._result = None
        self._exc_info = ()

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def run(self):
        try:
            timeout = self.kwargs.pop("timeout", 0)
            if timeout:
                timer = Timeout(timeout)
                timer.start()
            self._result = self._run(*self.args, **self.kwargs)
            self._future.set_result(self._result)
        except:
            self._exc_info = sys.exc_info()
            self._future.set_exc_info(self._exc_info)
        finally:
            if timeout:
                timer.cancel()

    def start(self):
        self.switch()

    def __str__(self):
        func_name = "%s of %s " % (self._run.__name__, self._run.__module__)
        return "<greenlet %s at %s>" % (func_name, hex(id(self)))

    def __repr__(self):
        return self.__str__()

    def wait(self):
        return self._future

    @classmethod
    def spawn(cls_green, *args, **kwargs):
        task = cls_green(*args, **kwargs)
        task.start()
        return task


def spawn(callable_obj, *args, **kwargs):
    return GreenTask.spawn(callable_obj, *args, **kwargs).wait()


class TimeoutException(Exception):
    pass


class Timeout(object):
    def __init__(self, deadline, ex=TimeoutException):
        self._greenlet = greenlet.getcurrent()
        self._ex = ex
        self._callback = None
        self._deadline = deadline
        self._delta = time.time() + deadline
        self._ioloop = IOLoop.current()

    def start(self, callback=None):
        errmsg = "%s timeout, deadline is %d seconds" % (
                str(self._greenlet), self._deadline)
        if callback:
            self._callback = self._ioloop.add_timeout(self._delta, 
                                                      callback,
                                                      self._ex(errmsg))
        else:
            self._callback = self._ioloop.add_timeout(self._delta, 
                                                      self._greenlet.throw,
                                                      self._ex(errmsg))

    def cancel(self):
        assert self._callback, "Timeout not started"
        self._ioloop.remove_timeout(self._callback)
        self._greenlet = None
