# -*- coding: utf-8 -*-

from scloud.utils.error_code import ERROR

class SystemError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    def __unicode__(self):
        return self.message


class NotFoundError(Exception):
    def __init__(self):
        self.code = ERROR.not_found_err.errcode
        self.message = ERROR.not_found_err.errvalue

    def __unicode__(self):
        return self.message

