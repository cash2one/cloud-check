#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import scloud
from scloud.shortcuts import url
from scloud.shortcuts import *
from scloud.handlers import Handler
import requests
import urlparse
import urllib
import urllib2
import time


@url("/event/index", name="event.index", active="event.index")
class GuideHandler(Handler):
    u'事件管理'
    def get(self):
        data = {}
        return self.render("admin/event/index.html", **data)


@url("/event/add", name="event.add", active="event.add")
class GuideHandler(Handler):
    u'添加事件'
    def get(self):
        data = {}
        return self.render("admin/event/add.html", **data)
