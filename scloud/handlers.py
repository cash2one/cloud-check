#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from torweb.handlers import BaseHandler
from scloud.shortcuts import env


class Handler(BaseHandler):
    def __str__(self):
        return self.__doc__ or self.__class__.__name__

    def prepare(self):
        self.pjax = self.request.headers.get("X-PJAX")

    def render_to_string(self, template, **kwargs):
        tmpl = env.get_template(template)
        kwargs.update({
            "handler": self,
            "request": self.request,
            "reverse_url": self.application.reverse_url
        })
        template_string = tmpl.render(**kwargs)
        return template_string

    def render(self, template, **kwargs):
        if self.pjax:
            template_string = self.render_to_string("%s_pjax.html" % template.split(".html")[0], **kwargs)
        else:
            template_string = self.render_to_string(template, **kwargs)
        self.write(template_string)
