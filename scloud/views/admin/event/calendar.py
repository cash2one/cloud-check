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


@url("/event/calendar", name="event.calendar", active="calendar")
class GuideHandler(Handler):
    u'日历事件'
    def get(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/event/calendar.html", **data)
