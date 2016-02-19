# -*- coding: utf-8 -*-

from tornado.util import ObjectDict
from scloud.shortcuts import env
from scloud.config import CONF


class BaseService(object):
    def __init__(self, db, params={}, handler=None):
        self.db = db
        self.params = params
        self.handler = handler

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

    def render_to_string(self, template, **kwargs):
        tmpl = env.get_template(template)
        kwargs.update({
            "CONF": CONF,
            "handler": self.handler,
            "request": self.handler.request,
            "reverse_url": self.handler.application.reverse_url
        })
        template_string = tmpl.render(**kwargs)
        return template_string
