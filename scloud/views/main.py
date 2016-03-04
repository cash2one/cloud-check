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


@url("/", name="index", active="index1")
class Index1Handler(Handler):
    u'首页'
    def get(self):
        return self.redirect(self.reverse_url("user_profile"))


@url("/index2", name="index2", active="index2")
class Index2Handler(Handler):
    u'主页'
    def get(self):
        data = {"name": "main"}
        # time.sleep(1)
        return self.render("admin/index2.html", **data)

@url("/topic", name="topic")
class MainHandler(Handler):
    def get(self):
        data = {"name": "topic"}
        return self.render("topic.html", **data)

@url("/main.php/live/reward", name="reward")
@url("/main.php/live/partyList", name="partyList")
class PartyList(Handler):
    def post(self):
        p = self.args
        p["event_point"] = "1000"

        headers = self.request.headers
        del headers["Proxy-Connection"]
        del headers["Connection"]
        del headers["X-Scheme"]
        del headers["X-Real-IP"]
        print headers
        post_url = urlparse.urljoin(CONFIG("DOMAIN"), self.reverse_url(self.kwargs["name"]))
        logger.info(post_url)
        #response = requests.post(post_url, data=params, headers=self.request.headers)
        params = urllib.urlencode(p)
        logger.info("CALLBACK_REQ_DATA: %s" % params)
        req = urllib2.Request(url=post_url, data=params, headers=headers)
        from code import interact
        #interact(local=locals())
        logger.info("*****CALLBACK_REQ_ALL: %s" % str(post_url + "?" + params))
        req_start = time.time()
        response = urllib2.urlopen(req).read()
        logger.info("*****callback response: %s" % response)
        #response = response.decode('utf-8')
        req_end = time.time()
        logger.info("CALLBACK_REQ_TIME: START:[%s]_____END:[%s]_____USE:[%s]" % (req_start, req_end, req_end - req_start))
        logger.info("CALLBACK_RESPONSE: %s" % response)

        logger.info(response)
        self.write(response)
