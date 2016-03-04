# -*- coding: utf-8 -*-

import scloud
from torweb.urls import url
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
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
from scloud.services.svc_profile import ProfileService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError


@url("/user/profile", name="user_profile", active="user_profile")
class ProfileHandler(AuthHandler):
    def get_index_page(self, **kwargs):
        svc = ActHistoryService(self, kwargs)
        act_histories_res = svc.get_list()
        apply_tasks_res = svc.get_res_tasks()
        if isinstance(act_histories_res, Exception):
            raise act_histories_res
        data = {
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "act_histories_res": act_histories_res,
            "apply_tasks_res": apply_tasks_res
        }
        return data

    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/user/profile/index.html", **data)


@url("/task/(?P<task_id>\d+)/confirm_start_date", name="task_confirm", active="user_profile")
class TaskConfirmHandler(ProfileHandler):
    @unblock
    def post(self, **kwargs):
        svc = ActHistoryService(self, kwargs)
        confirm_res = svc.confirm_start_date()
        if isinstance(confirm_res, Exception):
            raise confirm_res
        self.add_message(u"已确认用户信息")
        data = self.get_index_page(**kwargs)
        tmpl = self.render_to_string("admin/user/profile/index_pjax.html", **data)
        logger.info(tmpl)
        return simplejson.dumps(self.success(data=tmpl))

