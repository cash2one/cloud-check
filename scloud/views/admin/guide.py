# -*- coding: utf-8 -*-

import scloud
from torweb.urls import url
from scloud.shortcuts import *
from scloud.handlers import Handler
import requests
import urlparse
import urllib
import urllib2
import time


@url("/guide", name="guide", active="guide")
class GuideHandler(Handler):
    u'申请资源'
    def get(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/index.html", **data)


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