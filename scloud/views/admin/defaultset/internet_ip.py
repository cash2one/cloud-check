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
from scloud.services.svc_env_internet_ip import EnvInternetIpService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.defaultset.env_info import BaseEnvHandler
from scloud.models.environment import Env_Internet_Ip_Types


@url("/defaultset/env_internet_ip", name="defaultset.env_internet_ip", active="defaultset.env_internet_ip")
class Env_Internet_Ip_Handler(BaseEnvHandler):
    u"""环境设置"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_internet_ip/index.html", **data)


class BaseEnvInternetIpHandler(BaseEnvHandler):
    def get_index_page(self, **kwargs):
        data = super(BaseEnvInternetIpHandler, self).get_index_page()
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        env_internet_ip_types = env_res.data.env_internet_ip_types
        page = self.getPage(env_internet_ip_types)
        data.update({
            "Env_Internet_Ip_Types": Env_Internet_Ip_Types,
            "env_res": env_res,
            "page": page
        })
        return data


@url("/defaultset/env_internet_ip/(?P<env_id>\d+)/list", name="defaultset.env_internet_ip.list", active="defaultset.env_internet_ip")
class Env_Internet_Ip_Handler(BaseEnvInternetIpHandler):
    u"""环境设置"""
    @unblock
    def get(self, **kwargs):
        data = self.get_index_page(**kwargs)
        return self.render_to_string("admin/defaultset/env_internet_ip/list.html", **data)


@url("/defaultset/env_internet_ip/(?P<env_id>\d+)/add", name="defaultset.env_internet_ip.add", active="defaultset.env_internet_ip")
class Add_Env_Internet_Ip_Handler(BaseEnvInternetIpHandler):
    u"""添加新IP分类"""
    @unblock
    def get(self, **kwargs):
        data = self.get_index_page(**kwargs)
        return self.render_to_string("admin/defaultset/env_internet_ip/add.html", **data)

    @unblock
    def post(self, **kwargs):
        svc = EnvInternetIpService(self, kwargs)
        env_internet_ip_res = svc.add_env_internet_ip()
        data = self.get_index_page(**kwargs)
        data.update({
            "env_internet_ip_res": env_internet_ip_res
        })
        if env_internet_ip_res.return_code == 0:
            self.add_message(u"环境[%s]对应互联网IP类型[%s]添加成功！" % (env_internet_ip_res.data.env.name, env_internet_ip_res.data.name), level="success", post_action=True)
            tmpl = self.render_to_string("admin/defaultset/env_internet_ip/list_pjax.html", **data)
        else:
            # self.add_message(env_res.return_message, level="warning")
            tmpl = self.render_to_string("admin/defaultset/env_internet_ip/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/defaultset/env/(?P<env_id>\d+)/internet_ip/(?P<env_internet_ip_id>\d+)/edit", name="defaultset.env_internet_ip.edit", active="defaultset.env_internet_ip")
class Add_Env_Internet_Ip_Handler(BaseEnvInternetIpHandler):
    u"""编辑互联网IP分类"""
    @unblock
    def get(self, **kwargs):
        # svc = EnvService(self, kwargs)
        # env_res = svc.get_env()
        data = self.get_index_page(**kwargs)
        svc = EnvInternetIpService(self, kwargs)
        env_internet_ip_res = svc.get_env_internet_ip()
        data.update({
            "env_internet_ip_res": env_internet_ip_res
        })
        data.update(kwargs)
        return self.render_to_string("admin/defaultset/env_internet_ip/edit.html", **data)

    @unblock
    def post(self, **kwargs):
        data = self.get_index_page(**kwargs)
        svc = EnvInternetIpService(self, kwargs)
        env_internet_ip_res = svc.edit_env_internet_ip()
        data.update({
            "env_internet_ip_res": env_internet_ip_res
        })
        data.update(kwargs)
        if env_internet_ip_res.return_code == 0:
            self.add_message(u"环境[%s]对应互联网IP类型[%s]修改成功！" % (env_internet_ip_res.data.env.name, env_internet_ip_res.data.name), level="success", post_action=True)
            tmpl = self.render_to_string("admin/defaultset/env_internet_ip/list_pjax.html", **data)
        else:
            # self.add_message(env_res.return_message, level="warning")
            tmpl = self.render_to_string("admin/defaultset/env_internet_ip/edit_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/defaultset/env_internet_ip/(?P<env_id>\d+)/del", name="defaultset.env_internet_ip.del", active="defaultset.env_internet_ip")
class Env_Internet_Ip_Del_Handler(BaseEnvInternetIpHandler):
    u"""删除互联网IP类型"""
    @unblock
    def delete(self, **kwargs):
        env_internet_ip_ids = self.get_arguments("env_internet_ip_id")
        kwargs["env_internet_ip_ids"] = env_internet_ip_ids
        svc = EnvInternetIpService(self, kwargs)
        env_internet_ip_res = svc.del_env_internet_ip()
        data = self.get_index_page(**kwargs)
        if env_internet_ip_res.return_code == 0:
            for ip in env_internet_ip_res.data:
                self.add_message(u"环境[%s]对应互联网IP类型[%s]删除成功！" % (ip.env.name, ip.name), level="success", post_action=False)
        tmpl = self.render_to_string("admin/defaultset/env_internet_ip/list_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
