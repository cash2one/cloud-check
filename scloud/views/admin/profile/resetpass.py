# -*- coding: utf-8 -*-

import scloud
from scloud.shortcuts import url
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


@url("/user/resetpass", name="user_resetpass", active="user_resetpass")
class ProfileHandler(AuthHandler):
    u"""充值密码"""

    @unblock
    def get(self):
        return self.render_to_string("admin/profile/resetpass/index.html")
