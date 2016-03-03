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
    @unblock
    def get(self):
        svc = ActHistoryService(self)
        act_histories_res = svc.get_list()
        apply_tasks_res = svc.get_res_tasks()
        if isinstance(act_histories_res, Exception):
            raise act_histories_res
        data = {
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "act_histories_res": act_histories_res,
            "apply_tasks_res": apply_tasks_res
        }
        return self.render_to_string("admin/user/profile/index.html", **data)


@url("/task/(?P<task_id>\d+)/confirm_start_date", name="task_confirm", active="user_profile")
class TaskConfirmHandler(AuthHandler):
    @unblock
    def post(self, **kwargs):
        svc = ActHistoryService(self, kwargs)
        confirm_res = svc.confirm_start_date()
        if isinstance(confirm_res, Exception):
            raise confirm_res
        return simplejson.dumps(self.success(data=confirm_res))
