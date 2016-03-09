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

class BaseEnvHandler(AuthHandler):
    def get_index_page(self):
        svc = EnvService(self)
        env_list_res = svc.get_list()
        page = self.getPage(env_list_res.data)
        data = {
            "env_list_res": env_list_res,
            "page": page
        }
        return data
        

@url("/defaultset/env_info", name="defaultset.env_info", active="defaultset.env_info")
class Env_Info_Handler(BaseEnvHandler):
    u"""环境设置"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_info/index.html", **data)


@url("/defaultset/env_info/add", name="defaultset.env_info.add", active="defaultset.env_info")
class Add_Env_Info_Handler(BaseEnvHandler):
    u"""添加新环境"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_info/add.html", **data)

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
            tmpl = self.render_to_string("admin/defaultset/env_info/index_pjax.html", **data)
        else:
            # self.add_message(env_res.return_message, level="warning")
            tmpl = self.render_to_string("admin/defaultset/env_info/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/defaultset/env_info/(?P<env_id>\d+)/edit", name="defaultset.env_info.edit", active="defaultset.env_info")
@url("/defaultset/env_info/edit", name="defaultset.env_info.edit_info", active="defaultset.env_info")
class Add_Env_Info_Handler(BaseEnvHandler):
    u"""编辑环境"""
    @unblock
    def get(self, **kwargs):
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        data = self.get_index_page()
        data.update({
            "env_res": env_res
        })
        return self.render_to_string("admin/defaultset/env_info/edit.html", **data)

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
            tmpl = self.render_to_string("admin/defaultset/env_info/index_pjax.html", **data)
        else:
            # self.add_message(env_res.return_message, level="warning")
            tmpl = self.render_to_string("admin/defaultset/env_info/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
