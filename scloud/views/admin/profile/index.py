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
        if isinstance(act_histories_res, Exception):
            raise act_histories_res
        data = {
            "act_histories_res": act_histories_res,
        }
        return self.render_to_string("admin/user/profile/index.html", **data)
