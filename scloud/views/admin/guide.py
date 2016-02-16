# -*- coding: utf-8 -*-

import scloud
from torweb.urls import url
from scloud.config import logger
from scloud.handlers import Handler, AuthHandler
import requests
import urlparse
import urllib
import urllib2
import simplejson
import time
from tornado.web import asynchronous
from tornado import gen
from scloud.utils.permission import check_perms
from scloud.services.svc_project import ProjectService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError


@url("/guide", name="guide", active="guide")
class GuideHandler(AuthHandler):
    u'申请资源'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self.svc.db, self.args)
        result = svc.get_project_list()
        if result.return_code < 0:
            raise SystemError(result.return_code, result.return_message)
        logger.info(result)
        return self.render_to_string("admin/guide/index.html", result=result)

    @check_perms('pro_info.insert')
    @unblock
    def post(self):
        svc = ProjectService(self.svc.db, self.args)
        result = svc.create_project()
        logger.info(result)
        if result.return_code == 0:
            logger.info("return_code:%s" % result.return_code)
            self.add_message(u"项目添加成功", level="success")
            return self.render_to_string("admin/guide/step1.html", result=result)
        else:
            logger.info("return_code:%s" % result.return_code)
            post_result = result
            proj_result = svc.get_project_list()
            self.add_message(post_result.return_message, level='warning')
            return self.render_to_string("admin/guide/index.html", result=proj_result, post_result=post_result)


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
class GuideStep2Handler(Handler):
    u'资源申请/变更 步骤1'
    def get(self):
        return self.post()

    def post(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/step2.html", **data)


@url("/guide/step/3", name="guide_step_3", active="guide")
class GuideStep3Handler(Handler):
    u'资源申请/变更 步骤1'
    def get(self):
        return self.post()

    def post(self):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/step3.html", **data)
