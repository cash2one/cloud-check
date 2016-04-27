# -*- coding: utf-8 -*-

import scloud
#from torweb.urls import url
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
from scloud.services.svc_project import ProjectService
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from .base import ApplyHandler


class GuideStepGetHandler(AuthHandler):
    def get_pro_info_res(self, pro_id):
        kw = {"pro_id": pro_id}
        svc = ProjectService(self, kw)
        pro_info_res = svc.get_project()
        if isinstance(pro_info_res, Exception):
            raise pro_info_res
        data = {
            "pro_info_res": pro_info_res,
            "STATUS_RESOURCE": STATUS_RESOURCE,
        }
        return data


@url("/apply/resource/index", name="apply.resource", active="apply.resource")
class GuideHandler(GuideStepGetHandler):
    u'权限申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        svc = ProResourceApplyService(self)
        pro_resource_applies_res = svc.get_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = dict(
            pro_list_res = pro_list_res,
            page = self.getPage(pro_resource_applies_res.data)
        )
        return self.render_to_string("admin/apply/resource/index.html", **data)


@url("/apply/resource/detail", name="apply.resource.detail", active="apply.resource")
class ProResourceDetailHandler(GuideStepGetHandler):
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )
    u'权限用户详情'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProResourceApplyService(self)
        pro_resource_apply_res = svc.get_resource()
        if pro_resource_apply_res.return_code < 0:
            raise SystemError(pro_resource_apply_res.return_code, pro_resource_apply_res.return_message)
        logger.info(pro_resource_apply_res)
        data = {
            "pro_resource_apply_res": pro_resource_apply_res,
        }
        return self.render_to_string("admin/apply/resource/detail.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/resource/add", name="apply.resource.add", active="apply.resource.add")
@url("/apply/resource/add", name="apply.resource.add", active="apply.resource")
@url("/apply/resource/edit", name="apply.resource.edit", active="apply.resource")
class GuideHandler(ApplyHandler):
    u'权限申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        if self.kwargs["name"] == "apply.resource.add":
            data = self.get_pro_data()
            return self.render_to_string("admin/apply/resource/add.html", **data)
        else:
            data = self.get_pro_data()
            svc = ProResourceApplyService(self)
            pro_resource_apply_res = svc.get_resource()
            svc = ProjectService(self)
            env_resource_value_res = svc.load_env_resource_values()
            env_internet_ip_types_res = svc.load_env_internet_ip_types()
            data.update(dict(
                pro_resource_apply_res = pro_resource_apply_res,
                env_internet_ip_types_res = env_internet_ip_types_res,
                env_resource_value_res = env_resource_value_res,
            ))
            return self.render_to_string("admin/apply/resource/edit.html", **data)

    @unblock
    def post(self):
        kw = {"user_id": self.current_user.id}
        svc = ProResourceApplyService(self, kw)
        # pro_svc = ProjectService(self, kw)
        # pro_info_res = pro_svc.get_project()
        if self.kwargs["name"] == "apply.resource.add":
            pro_resource_apply_res = svc.do_apply()
        else:
            pro_resource_apply_res = svc.do_re_apply()
        pro_info_data = self.get_pro_data(pro_id=self.args.get("pro_id"))
        data = {
            "pro_resource_apply_res": pro_resource_apply_res
        }
        svc = ProjectService(self)
        env_resource_value_res = svc.load_env_resource_values()
        env_internet_ip_types_res = svc.load_env_internet_ip_types()
        data.update(dict(
            env_internet_ip_types_res = env_internet_ip_types_res,
            env_resource_value_res = env_resource_value_res,
        ))

        data.update(pro_info_data)
        if pro_resource_apply_res.return_code == 0:
            self.add_message(u"申请项目[%s-%s]资源成功！" % (pro_resource_apply_res.data.project.name, pro_resource_apply_res.data.desc), level="success", post_action=True)
            tmpl = self.render_to_string("admin/apply/resource/detail_pjax.html", **data)
        else:
            self.add_message(u"申请项目资源失败！(%s)%s" % (pro_resource_apply_res.return_code, pro_resource_apply_res.return_message), level="warning")
            tmpl = self.render_to_string("admin/guide/_step_1_res_add.html", **data)
        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/resource/load_env", name="apply.resource.load_env", active="apply.resource")
class ResourceLoadEnvHandler(AuthHandler):
    @unblock
    def get(self, **kwargs):
        svc = ProjectService(self)
        env_resource_value_res = svc.load_env_resource_values()
        env_internet_ip_types_res = svc.load_env_internet_ip_types()
        data = dict(
            env_internet_ip_types_res = env_internet_ip_types_res,
            env_resource_value_res = env_resource_value_res,
        )
        env_internet_ip_types_tmpl = self.render_to_string("admin/apply/resource/_env_internet_ip_types.html", **data)
        return simplejson.dumps(self.success(data=dict(
            env_resource_value = env_resource_value_res.data,
            env_internet_ip_types_tmpl = env_internet_ip_types_tmpl
        )))


@url("/apply/resource/generate_fee", name="apply.resource.generate_fee", active="apply.resource")
class GuideGenerateFeeHandler(ApplyHandler):
    @unblock
    def post(self, **kwargs):
        data = self.get_pro_data()
        svc = ProResourceApplyService(self, self.args)
        fee_res = svc.generate_fee()
        svc = ProjectService(self)
        env_resource_value_res = svc.load_env_resource_values()
        env_internet_ip_types_res = svc.load_env_internet_ip_types()
        data.update(dict(
            fee_res = fee_res,
            env_internet_ip_types_res = env_internet_ip_types_res,
            env_resource_value_res = env_resource_value_res,
        ))
        # logger.info(fee_res)
        tmpl = self.render_to_string("admin/apply/resource/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/apply/resource/del", name="apply.resource.del", active="apply.resource")
class ApplyResourceDelHandler(GuideStepGetHandler):
    u'删除用户'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        user_id_list = self.get_arguments("user_id")
        svc = ProUserService(self, {"user_id_list": user_id_list})
        del_res = svc.do_del_pro_user()
        logger.info(del_res)
        if del_res.return_code == 0:
            self.add_message(u"用户信息删除成功！", level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"用户信息删除失败！(%s)(%s)" % (del_res.return_code, del_res.return_message), level="warning")
        data = self.get_pro_data()
        svc = ProUserService(self, {"user_id": self.current_user.id})
        pro_users_res = svc.get_list()
        page = self.getPage(pro_users_res.data)
        data.update(page=page)
        tmpl = self.render_to_string("admin/apply/resource/index_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
