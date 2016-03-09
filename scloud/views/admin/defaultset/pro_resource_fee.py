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
from scloud.services.svc_env import EnvService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.defaultset.env_info import BaseEnvHandler


@url("/defaultset/env_resource_fee", name="defaultset.env_resource_fee", active="defaultset.env_resource_fee")
class Env_resource_fee_Handler(BaseEnvHandler):
    u"""资源申请费用设置"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_resource_fee/index.html", **data)


@url("/defaultset/env_resource_fee/add", name="defaultset.env_resource_fee.add", active="defaultset.env_resource_fee")
class Add_Env_resource_fee_Handler(BaseEnvHandler):
    u"""添加新资源费用"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_resource_fee/add.html", **data)

    @unblock
    def post(self):
        svc = EnvService(self)
        env_res = svc.add_env()
        data = self.get_index_page()
        data.update({
            "env_res": env_res
        })
        if env_res.return_code == 0:
            self.add_message(u"新环境[%s]添加成功！" % env_res.data.name, level="success", post_action=True)
            tmpl = self.render_to_string("admin/defaultset/env_resource_fee/index_pjax.html", **data)
        else:
            # self.add_message(env_res.return_message, level="warning")
            tmpl = self.render_to_string("admin/defaultset/env_resource_fee/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/defaultset/env_resource_fee/(?P<env_id>\d+)/edit", name="defaultset.env_resource_fee.edit", active="defaultset.env_resource_fee")
class Add_Env_resource_fee_Handler(BaseEnvHandler):
    u"""编辑资源申请费用"""
    @unblock
    def get(self, **kwargs):
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        data = self.get_index_page()
        data.update({
            "env_res": env_res
        })
        return self.render_to_string("admin/defaultset/env_resource_fee/edit.html", **data)

    @unblock
    def post(self, **kwargs):
        svc = EnvService(self, kwargs)
        env_res = svc.edit_env()
        data = self.get_index_page()
        data.update({
            "env_res": env_res
        })
        if env_res.return_code == 0:
            self.add_message(u"新环境[%s]修改成功！" % env_res.data.name, level="success", post_action=True)
            tmpl = self.render_to_string("admin/defaultset/env_resource_fee/index_pjax.html", **data)
        else:
            # self.add_message(env_res.return_message, level="warning")
            tmpl = self.render_to_string("admin/defaultset/env_resource_fee/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
