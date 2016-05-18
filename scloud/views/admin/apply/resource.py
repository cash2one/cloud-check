# -*- coding: utf-8 -*-

import scloud
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger, thrownException, logThrown
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
from scloud.services.svc_env_internet_ip import EnvInternetIpService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.utils.error_code import ERROR
from .base import ApplyHandler
from scloud.async_services.publish_task import publish_notice_checker


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
class ProResourceApplyIndexHandler(GuideStepGetHandler):
    u'资源申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        logger.info(pro_list_res)
        svc = ProResourceApplyService(self)
        pro_resource_applies_res = svc.get_list()
        pro_resource_apply_list = pro_resource_applies_res.data
        logger.info(pro_resource_apply_list)
        data = dict(
            pro_list_res = pro_list_res,
            page = self.getPage(pro_resource_apply_list)
        )
        return self.render_to_string("admin/apply/resource/index.html", **data)


@url("/apply/resource/detail", name="apply.resource.detail", active="apply.resource")
class ProResourceDetailHandler(GuideStepGetHandler):
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )
    u'资源申请详情'
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


@url("/apply/resource/add", name="apply.resource.add", active="apply.resource")
@url("/apply/resource/edit", name="apply.resource.edit", active="apply.resource")
@url("/apply/resource/revoke", name="apply.resource.revoke", active="apply.resource")
@url("/apply/resource/pay", name="apply.resource.pay", active="apply.resource")
class DoProResourceApplyHandler(ApplyHandler):
    u'资源申请'
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
            if self.kwargs["name"] == "apply.resource.pay":
                data.update(dict(pro_resource_apply_res=pro_resource_apply_res))
                return self.render_to_string("admin/apply/resource/pay.html", **data)
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
            post_action = u"提交"
            pro_resource_apply_res = svc.do_apply()
        elif self.kwargs["name"] == "apply.resource.edit":
            post_action = u"重新提交"
            pro_resource_apply_res = svc.do_re_apply()
        elif self.kwargs["name"] == "apply.resource.revoke":
            post_action = u"撤销"
            pro_resource_apply_res = svc.do_revoke()
        elif self.kwargs["name"] == "apply.resource.pay":
            post_action = u"支付"
            pro_resource_apply_res = svc.do_pay()
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
            self.add_message(u"申请项目[%s-%s]%s资源成功！" % (pro_resource_apply_res.data.project.name, pro_resource_apply_res.data.desc, post_action), level="success", post_action=True)
            publish_notice_checker.delay(self.current_user.id)
            if self.kwargs["name"] == "apply.resource.pay":
                tmpl = self.render_to_string("admin/guide/_step_2_pay_detail.html", **data)
            else:
                tmpl = self.render_to_string("admin/guide/_step_1_res_detail.html", **data)
        else:
            self.add_message(u"申请项目%s资源失败！(%s)%s" % (post_action, pro_resource_apply_res.return_code, pro_resource_apply_res.return_message), level="warning")
            if self.kwargs["name"] == "apply.resource.pay":
                tmpl = self.render_to_string("admin/guide/_step_2_pay.html", **data)
            else:
                tmpl = self.render_to_string("admin/guide/_step_1_res_add.html", **data)
        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/resource/load_env", name="apply.resource.load_env", active="apply.resource")
class ResourceLoadEnvHandler(ApplyHandler):
    @unblock
    def get(self, **kwargs):
        data = self.get_pro_data()
        svc = ProjectService(self)
        env_resource_value_res = svc.load_env_resource_values()
        env_internet_ip_types_res = svc.load_env_internet_ip_types()
        svc = ProResourceApplyService(self, self.args)
        pro_resource_apply_res = svc.get_resource()
        pro_resource_apply = pro_resource_apply_res.data if pro_resource_apply_res.return_code == 0 else None
        internet_ip_options = env_internet_ip_types_res.data if env_internet_ip_types_res.return_code == 0 else []
        internet_ip_value = 0
        if pro_resource_apply:
            internet_ip_value = pro_resource_apply.internet_ip
        else:
            if env_resource_value_res.return_code == 0:
                internet_ip_value = env_resource_value_res.data["internet_ip"]
        try:
            # internet_bandwidths = []
            # for i in internet_ip_options:
            #     logger.info("internet_ip: %s, value: %s" % (i["value"], internet_ip_value))

            internet_bandwidths = {internet_ip_value: i["bandwidths"] for i in internet_ip_options if int(i["value"]) == int(internet_ip_value)}[internet_ip_value]
            # logger.info(internet_bandwidths)
        except:
            logThrown()
            internet_bandwidths = []
        data.update(dict(
            env_internet_ip_types_res = env_internet_ip_types_res,
            env_resource_value_res = env_resource_value_res,
            pro_resource_apply = pro_resource_apply,
            internet_bandwidths = internet_bandwidths
        ))
        env_internet_ip_types_tmpl = self.render_to_string("admin/apply/resource/_env_internet_ip_types.html", **data)
        env_internet_bandwidth_tmpl = self.render_to_string("admin/apply/resource/_env_internet_bandwidth.html", **data)
        return simplejson.dumps(self.success(data=dict(
            env_resource_value = env_resource_value_res.data,
            env_internet_ip_types_tmpl = env_internet_ip_types_tmpl,
            env_internet_bandwidth_tmpl = env_internet_bandwidth_tmpl
        )))


@url("/apply/resource/load_bandwidth", name="apply.resource.load_bandwidth")
class ProBackupDetailHandler(ApplyHandler):
    u'加载互联网宽带'
    @unblock
    def get(self, **kwargs):
        svc = EnvInternetIpService(self)
        internet_bandwidths_res = svc.get_internet_bandwidths()
        if internet_bandwidths_res.return_code == 0:
            internet_bandwidths = internet_bandwidths_res.data
        else:
            internet_bandwidths = []
        data = self.get_pro_data()
        data.update({
            "internet_bandwidths": internet_bandwidths,
        })
        # logger.info(pro_backup_res.data)
        return self.render_to_string("admin/apply/resource/_env_internet_bandwidth.html", **data)

@url("/apply/resource/generate_fee", name="apply.resource.generate_fee", active="apply.resource")
class GuideGenerateFeeHandler(ApplyHandler):
    "资源申请费用试算"
    @unblock
    def post(self, **kwargs):
        data = self.get_pro_data()
        svc = ProResourceApplyService(self, self.args)
        pro_resource_apply_res = svc.get_resource()
        logger.info("[pro_resource_apply_res] %s" % pro_resource_apply_res)
        fee_res = svc.generate_fee()
        svc = ProjectService(self)
        env_resource_value_res = svc.load_env_resource_values()
        env_internet_ip_types_res = svc.load_env_internet_ip_types()
        data.update(dict(
            fee_res = fee_res,
            pro_resource_apply_res = pro_resource_apply_res,
            env_internet_ip_types_res = env_internet_ip_types_res,
            env_resource_value_res = env_resource_value_res,
        ))
        logger.info(fee_res)
        if fee_res.return_code == 0:
            self.add_message(u"费用计算成功！单月费用 %s（元/月）×有效期 %s（月）=总费用 %s（元）" % (fee_res.data["unit_fee"], self.args.get('period'), fee_res.data["total_fee"]), level="success")
        else:

            if fee_res.return_code == ERROR.database_save_err.errcode:
                return_messages = fee_res.return_messages
                self.add_message(u"费用计算失败！", level="warning")
                for msg in return_messages:
                    self.add_message(u"%s" % msg, level="warning")
            else:
                self.add_message(u"费用计算失败！ %s(%s)" % (fee_res.return_code, fee_res.return_message), level="warning")

        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        tmpl = self.render_to_string("admin/guide/_step_1_res_form.html", **data)
        # tmpl = self.render_to_string("admin/apply/resource/add_pjax.html", **data)
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/resource/delete", name="apply.resource.del", active="guide")
class ProResourceDeleteHandler(ApplyHandler):
    u"""删除资源申请"""
    @check_perms('pro_resource_apply.delete')
    @unblock
    def post(self, **kwargs):
        svc = ProResourceApplyService(self, kwargs)
        delete_res = svc.do_delete()
        pro_resource_applies_res = svc.get_list()
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        # svc = ProResourceApplyService(self)
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = dict(
            pro_list_res = pro_list_res,
            page = self.getPage(pro_resource_applies_res.data)
        )
        if isinstance(delete_res, Exception):
            raise delete_res
        # data = self.get_pro_info_res(kwargs["pro_id"])
        if delete_res.return_code == 0:
            self.add_message("云资源[%s-%s]记录删除成功！"% (delete_res.data.project.name, delete_res.data.desc), level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message("云资源记录删除失败！(%s)%s"% (delete_res.return_code, delete_res.return_message), level="warning")
        # logger.info("\t [data]: %s" % data )
        # logger.info("\t [data pro_info_res]: %s" % data["pro_info_res"])
        tmpl = self.render_to_string("admin/apply/resource/index_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/apply/resource/pay_history", name="apply.resource.pay_history", active="apply.resource")
class ProResourcePayHistoryHandler(ApplyHandler):
    u"""资源申请支付历史"""
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self):
        data = self.get_pro_data(pro_id=self.args.get("pro_id"))
        svc = ProResourceApplyService(self)
        pro_resource_apply_res = svc.get_resource()
        data.update(dict(pro_resource_apply_res=pro_resource_apply_res))
        return self.render_to_string("admin/apply/resource/pay_history.html", **data)
