# -*- coding: utf-8 -*-


class SystemError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    def __unicode__(self):
        return self.message

