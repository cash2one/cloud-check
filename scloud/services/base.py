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

    def failure(self, return_code, return_message):
        result = ObjectDict()
        result.return_code = return_code
        result.return_message = return_message
        result.data = None
        return result
