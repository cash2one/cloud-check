# -*- coding: utf-8 -*-

from tornado.util import ObjectDict


class BaseService(object):
    def __init__(self, db, params={}):
        self.db = db
        self.params = params

    def success(self, data=None):
        result = ObjectDict()
        result.return_code = 0
        result.return_message = u""
        result.data = data
        return result

    def failure(self, error_obj):
        result = ObjectDict()
        result.return_code = error_obj.errcode
        result.return_message = error_obj.errvalue
        result.data = None
        return result
