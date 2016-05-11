# -*- coding: utf-8 -*-

import re
from tornado.util import ObjectDict
from scloud.shortcuts import env
from scloud.config import CONF, logger
from scloud.utils.error_code import ERROR
from scloud.config import logger, thrownException
from voluptuous import MultipleInvalid


class BaseService(object):
    def __init__(self, handler, params=None):
        self.db = handler.db
        self.handler = handler
        self.params = {}
        if handler and hasattr(handler, "args"):
            self.params.update(self.handler.args)
        else:
            setattr(handler, "args", {})
        if params:
            self.params.update(params)
        else:
            self.params.update({})
        logger.info("self.params : %s" % self.params)
        # if handler:
        #     logger.info("handler args :%s" % self.handler.args)

    @thrownException
    def email_check(self,email):
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return 1
        return 0

    def success(self, data=None):
        result = ObjectDict()
        result.return_code = 0
        result.return_message = u""
        result.data = data
        return result

    def failure(self, error_obj, data=None):
        result = ObjectDict()
        result.return_code = error_obj.errcode
        result.return_message = error_obj.errvalue
        result.data = data
        return result

    def failures(self, failure_list, data=None):
        result = ObjectDict()
        result.return_code = ERROR.database_save_err.errcode
        # result.return_message = u",".join(["(%s)%s" % (f.return_code, f.return_message) for f in failure_list])
        result.return_message = u"\n,".join([f for f in failure_list])
        result.return_messages = failure_list
        result.data = data
        return result

    def render_to_string(self, template, **kwargs):
        # return self.handler.render_to_string(template, **kwargs)
        tmpl = env.get_template(template)
        kwargs.update({
            "CONF": CONF,
            "getattr": getattr,
            "handler": self.handler,
            "request": self.handler.request,
            "reverse_url": self.handler.application.reverse_url
        })
        template_string = tmpl.render(**kwargs)
        return template_string

    def check_schema(self, schema):
        try:
            check_result = schema(self.params)
            return self.success()
        except MultipleInvalid as e:
            # logger.error(u"\t %s" % e.errors)
            ziped_errors = [(i.path[0], i) for i in e.errors]
            return self.failures(ziped_errors)
