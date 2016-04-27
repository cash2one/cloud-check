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
from scloud.services.svc_env import EnvService
from scloud.services.svc_env_resource_value import EnvResourceValueService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.defaultset.env_info import BaseEnvHandler
from scloud.models.environment import Env_Resource_Value

class Base_Env_Resource_Value_Handler(BaseEnvHandler):
    def get_index_page(self, **kwargs):
        data = super(Base_Env_Resource_Value_Handler, self).get_index_page()
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        internet_ips = env_res.data.env_internet_ip_types
        internet_ip_options = [{"value": i.id, "desc": i.name} for i in internet_ips]
        internet_ip_options.insert(0, {"value": 0, "desc": u"无需"})
        data.update({
            "Env_Resource_Value": Env_Resource_Value,
            "env_res": env_res,
            "internet_ip_options": internet_ip_options,
            "resource_value": env_res.data.env_resource_value,
        })
        return data


@url("/defaultset/env_resource_value", name="defaultset.env_resource_value", active="defaultset.env_resource_value")
class Env_resource_value_Handler(BaseEnvHandler):
    u"""资源申请推荐数据设置"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_resource_value/index.html", **data)


@url("/defaultset/env_resource_value/(?P<env_id>\d+)/edit", name="defaultset.env_resource_value.edit", active="defaultset.env_resource_value")
class Add_Env_resource_value_Handler(Base_Env_Resource_Value_Handler):
    u"""编辑资源申请推荐数据"""
    @unblock
    def get(self, **kwargs):
        data = self.get_index_page(**kwargs)

        svc = EnvResourceValueService(self, kwargs)
        resource_value_res = svc.get_env_resource_value()
        data.update({
            "resource_value_res": resource_value_res
        })
        return self.render_to_string("admin/defaultset/env_resource_value/edit.html", **data)

    @unblock
    def post(self, **kwargs):
        svc = EnvResourceValueService(self, kwargs)
        env_resource_value_res = svc.get_or_create()
        data = self.get_index_page(**kwargs)
        data.update({
            "resource_value_res": env_resource_value_res,
        })
        logger.info(env_resource_value_res)
        if env_resource_value_res.return_code == 0:
            self.add_message(u"环境[%s]对应默认值修改成功！" % env_resource_value_res.data.env.name, level="success", post_action=True)
        else:
            self.add_message(u"环境默认值修改失败！(%s)%s" % (env_resource_value_res.return_code, env_resource_value_res.return_message), level="warning")
        tmpl = self.render_to_string("admin/defaultset/env_resource_value/edit_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
