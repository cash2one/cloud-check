# -*- coding: utf-8 -*-

import scloud
from torweb.urls import url
from scloud.config import logger
from scloud.handlers import Handler
import requests
import urlparse
import urllib
import urllib2
import simplejson
import time
from tornado.web import asynchronous
from tornado import gen
from scloud.async_services import svc_project


@url("/guide", name="guide", active="guide")
class GuideHandler(Handler):
    u'申请资源'
    @asynchronous
    @gen.coroutine
    def get(self):
        response = yield gen.Task(svc_project.get_project_list.apply_async, args=[])
        logger.info(response.result)
        data = {"result": response.result}
        # time.sleep(1)
        raise gen.Return(self.render("admin/guide/index.html", **data))


@url("/guide/step/1", name="guide_step_1", active="guide")
class GuideStep1Handler(Handler):
    u'资源申请/变更 步骤1'
    def get(self):
        return self.post()

    def post(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/step1.html", **data)


@url("/guide/step/2", name="guide_step_2", active="guide")
class GuideHandler(Handler):
    u'资源申请/变更 步骤1'
    def get(self):
        return self.post()

    def post(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/step2.html", **data)


@url("/guide/step/3", name="guide_step_3", active="guide")
class GuideHandler(Handler):
    u'资源申请/变更 步骤1'
    def get(self):
        return self.post()

    def post(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/step3.html", **data)