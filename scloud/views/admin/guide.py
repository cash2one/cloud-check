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
from scloud.services.svc_project import ProjectService
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError


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


@url("/guide", name="guide", active="guide")
class GuideHandler(GuideStepGetHandler):
    u'申请资源'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        result = svc.get_project_list()
        if result.return_code < 0:
            raise SystemError(result.return_code, result.return_message)
        logger.info(result)
        return self.render_to_string("admin/guide/index.html", result=result, pro_resource_apply_status_types=pro_resource_apply_status_types)

    @check_perms('pro_info.insert')
    @unblock
    def post(self):
        svc = ProjectService(self)
        result = svc.create_project()
        logger.info(result)
        if result.return_code == 0:
            logger.info("return_code:%s" % result.return_code)
            self.add_message(u"项目添加成功", level="success")
            data = self.get_pro_info_res(result.data.id)
            return self.render_to_string("admin/guide/step1.html", **data)
        else:
            logger.info("return_code:%s" % result.return_code)
            post_result = result
            proj_result = svc.get_project_list()
            self.add_message(post_result.return_message, level='warning')
            return self.render_to_string("admin/guide/index.html", result=proj_result, post_result=post_result)

@url("/guide/(?P<pro_id>\d+)/step/1/generate_fee", name="generate_fee", active="guide")
class GuideGenerateFeeHandler(AuthHandler):
    @unblock
    def get(self, **kwargs):
        svc = ProResourceApplyService(self, self.args)
        fee_res = svc.generate_fee()
        logger.info(fee_res)
        return simplejson.dumps(fee_res)


@url("/guide/(?P<pro_id>\d+)/step/1", name="guide_step_1", active="guide")
@url("/guide/(?P<pro_id>\d+)/step/1/re_apply/(?P<res_id>\d+)", name="guide_step_1.re_apply", active="guide")
class GuideStep1Handler(GuideStepGetHandler):
    u'资源申请/变更 步骤1'
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self, **kwargs):
        data = self.get_pro_info_res(kwargs["pro_id"])
        return self.render_to_string("admin/guide/step1.html", **data)

    @check_perms('pro_resource_apply.insert, pro_resource_apply.update')
    @unblock
    def post(self, **kwargs):
        return self.guide_step_1(**kwargs)

    def guide_step_1(self, **kwargs):
        kw = {"user_id": self.current_user.id}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self, kw)
        # pro_svc = ProjectService(self, kw)
        # pro_info_res = pro_svc.get_project()
        if self.kwargs["name"] == "guide_step_1":
            post_apply_res = svc.do_apply()
        else:
            post_apply_res = svc.do_re_apply()
        pro_info_data = self.get_pro_info_res(kw["pro_id"])
        data = {
            "post_apply_res": post_apply_res
        }
        data.update(pro_info_data)
        if post_apply_res.return_code == 0:
            self.add_message(u"申请项目资源成功！", level="success")
            return self.render_to_string("admin/guide/step2.html", **data)
        else:
            self.add_message(u"申请项目资源失败！(%s)%s" % (post_apply_res.return_code, post_apply_res.return_message), level="warning")
            return self.render_to_string("admin/guide/step1.html", **data)


@url("/guide/(?P<pro_id>\d+)/step/2", name="guide_step_2", active="guide")
class GuideStep2Handler(GuideStepGetHandler):
    u'资源申请/变更 步骤2'
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self, **kwargs):
        data = self.get_pro_info_res(kwargs["pro_id"])
        logger.info("\t [data]: %s" % data)
        return self.render_to_string("admin/guide/step2.html", **data)

@url("/guide/pro/(?P<pro_id>\d+)/payed", name="guide_step_2_payed")
class GuideStep2PayedHandler(GuideStepGetHandler):
    u'资源申请/变更 步骤2 完成支付'
    @check_perms('pro_resource_apply.update')
    @thrownException
    @unblock
    def post(self, **kwargs):
        kw = {}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self, kw)
        resource_action_res = svc.do_pay()
        if isinstance(resource_action_res, Exception):
            raise resource_action_res
        data = self.get_pro_info_res(kwargs["pro_id"])
        tmpl = self.render_to_string("admin/guide/step2_pjax.html", **data)

        return simplejson.dumps(self.success(data=tmpl))


@url("/guide/(?P<pro_id>\d+)/step/3", name="guide_step_3", active="guide")
class GuideStep3Handler(GuideStepGetHandler):
    u'资源申请/变更 步骤3'
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self, **kwargs):
        data = self.get_pro_info_res(kwargs["pro_id"])
        return self.render_to_string("admin/guide/step3.html", **data)

    def post(self, pro_id):
        data = {"name": "torweb"}
        # time.sleep(1)
        return self.render("admin/guide/step3.html", **data)


@url("/pro/(?P<pro_id>\d+)/resource/(?P<res_id>\d+)/revoke", name="resource_revoke", active="guide")
class ProResourceRevokeHandler(GuideStepGetHandler):
    u"""撤销资源申请"""
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self, **kwargs):
        svc = ProResourceApplyService(self, kwargs)
        resource_res = svc.get_resource()
        if isinstance(resource_res, Exception):
            raise resource_res
        data = self.get_pro_info_res(kwargs["pro_id"])
        return self.render_to_string("admin/guide/step1.html", **data)
    def post(self, **kwargs):
        kw = {"user_id": self.current_user.id}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self, kw)
        revoke_res = svc.do_revoke()
        kw.update({"pro_id": revoke_res.data.pro_id if revoke_res.return_code == 0 else 0})
        pro_svc = ProjectService(self, kw)
        pro_info_res = pro_svc.get_project()
        data = {
            "pro_info_res": pro_info_res,
            "post_apply_res": revoke_res
        }
        if revoke_res.return_code == 0:
            self.add_message(u"资源申请已撤销！", level="success")
            return self.render("admin/guide/step2.html", **data)
        else:
            self.add_message(u"资源申请撤销失败！(%s)%s" % (post_apply_res.return_code, post_apply_res.return_message), level="warning")
            return self.render("admin/guide/step1.html", **data)


@url("/demo/mail", name="demo.name")
class DemoMail(Handler):
    @unblock
    def get(self):
        return self.do_mail()

    def do_mail(self):
        kw = {"res_id": 10}
        svc = ProResourceApplyService(self, kw)
        resource_res = svc.get_resource()
        data = {
            "resource_apply": resource_res.data,
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "getattr": getattr
        }
        return self.render_to_string("admin/mail/pro_resource_apply_to_admin.html", **data)
