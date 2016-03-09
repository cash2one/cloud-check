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
from scloud.services.svc_env_resource_fee import EnvResourceFeeService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.defaultset.env_info import BaseEnvHandler
from scloud.models.environment import Env_Resource_Fee


@url("/defaultset/env_resource_fee", name="defaultset.env_resource_fee", active="defaultset.env_resource_fee")
class Env_resource_fee_Handler(BaseEnvHandler):
    u"""资源申请费用设置"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_resource_fee/index.html", **data)


class Base_Env_Resource_Fee_Handler(BaseEnvHandler):
    def get_index_page(self, **kwargs):
        data = super(Base_Env_Resource_Fee_Handler, self).get_index_page()
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        internet_ips = env_res.data.env_internet_ip_types
        internet_ip_options = [{"value": i.id, "desc": i.name} for i in internet_ips]
        internet_ip_options.insert(0, {"value": 0, "desc": u"无需"})
        env_resource_fee = env_res.data.env_resource_fee
        data.update({
            "Env_Resource_Fee": Env_Resource_Fee,
            "env_res": env_res,
            "internet_ip_options": internet_ip_options,
            "resource_fee": env_resource_fee.as_dict() if env_resource_fee else {},
        })
        return data


# @url("/defaultset/env_resource_fee/add", name="defaultset.env_resource_fee.add", active="defaultset.env_resource_fee")
# class Add_Env_resource_fee_Handler(BaseEnvHandler):
#     u"""添加新资源费用"""
#     @unblock
#     def get(self):
#         data = self.get_index_page()
#         return self.render_to_string("admin/defaultset/env_resource_fee/add.html", **data)
# 
#     @unblock
#     def post(self):
#         svc = EnvService(self)
#         env_res = svc.add_env()
#         data = self.get_index_page()
#         data.update({
#             "env_res": env_res
#         })
#         if env_res.return_code == 0:
#             self.add_message(u"新环境[%s]添加成功！" % env_res.data.name, level="success", post_action=True)
#             tmpl = self.render_to_string("admin/defaultset/env_resource_fee/index_pjax.html", **data)
#         else:
#             # self.add_message(env_res.return_message, level="warning")
#             tmpl = self.render_to_string("admin/defaultset/env_resource_fee/add_pjax.html", **data)
#         return simplejson.dumps(self.success(data=tmpl))


@url("/defaultset/env_resource_fee/(?P<env_id>\d+)/edit", name="defaultset.env_resource_fee.edit", active="defaultset.env_resource_fee")
class Add_Env_resource_fee_Handler(Base_Env_Resource_Fee_Handler):
    u"""编辑资源申请费用"""
    @unblock
    def get(self, **kwargs):
        data = self.get_index_page(**kwargs)
        return self.render_to_string("admin/defaultset/env_resource_fee/edit.html", **data)

    @unblock
    def post(self, **kwargs):
        svc = EnvResourceFeeService(self, kwargs)
        env_resource_fee_res = svc.get_or_create()
        data = self.get_index_page(**kwargs)
        data.update({
            "resource_fee_res": env_resource_fee_res,
        })
        if env_resource_fee_res.return_code == 0:
            self.add_message(u"环境[%s]相应费用修改成功！" % env_resource_fee_res.data.env.name, level="success", post_action=True)
        tmpl = self.render_to_string("admin/defaultset/env_resource_fee/edit_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
