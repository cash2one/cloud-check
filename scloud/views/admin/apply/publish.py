# -*- coding: utf-8 -*-

import scloud
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE, admin_emails
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
from scloud.services.svc_apply_publish import ApplyPublish 
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services.publish_task import publish_notice_checker
from scloud.async_services.svc_mail import sendMail
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.const import STATUS_PRO_TABLES
from .base import ApplyHandler


@url("/apply/publish/index", name="apply.publish", active="apply.publish")
class PublishIndexHandler(ApplyHandler):
    u'互联网发布'

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
            ]
        else:
            _bread_list = []
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        data = self.get_pro_data()
        svc = ApplyPublish(self, {"user_id": self.current_user.id})
        pro_publishs_res = svc.get_list()
        page = self.getPage(pro_publishs_res.data)
        data.update(page=page)
        return self.render_to_string("admin/apply/publish/index.html", **data)


@url("/apply/publish/detail", name="apply.publish.detail", active="apply.publish")
class PublishDetailHandler(ApplyHandler):
    u'互联网发布详情'
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
                {"urlspec": url.handlers_dict.get('apply.publish'), "url": self.session.get("from_url"), "icon": "internet-explorer"},
            ]
        else:
            _bread_list = [
                {"urlspec": url.handlers_dict.get('apply.publish'), "url": self.session.get("from_url"), "icon": "internet-explorer"},
            ]
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ApplyPublish(self)
        pro_publish_res = svc.get_publish()
        if pro_publish_res.return_code < 0:
            raise SystemError(pro_publish_res.return_code, pro_publish_res.return_message)
        logger.info(pro_publish_res)
        data = {
            "pro_publish_res": pro_publish_res,
        }
        return self.render_to_string("admin/apply/publish/detail.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/user/add", name="apply.user.add", active="apply.user.add")
@url("/apply/publish/add", name="apply.publish.add", active="apply.publish")
@url("/apply/publish/edit", name="apply.publish.edit", active="apply.publish")
class PublishAddHandler(ApplyHandler):
    u'互联网发布申请'

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
                {"urlspec": url.handlers_dict.get('apply.publish'), "url": self.session.get("from_url"), "icon": "internet-explore"},
            ]
        else:
            _bread_list = [
                {"urlspec": url.handlers_dict.get('apply.publish'), "url": self.session.get("from_url"), "icon": "internet-explore"},
            ]
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        # pro_id = self.args.get("pro_id")
        # user_id = self.args.get("user_id", 0)
        data = self.get_pro_data()
        action_url = self.reverse_url(self.kwargs["name"])
        data.update(action_url=action_url)
        if self.kwargs["name"] == "apply.publish.edit":
            svc = ApplyPublish(self)
            # pro_users_res = svc.get_list()
            pro_publish_res = svc.get_publish()
            data.update(pro_publish_res=pro_publish_res)
        return self.render_to_string("admin/apply/publish/add.html", **data)

    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ApplyPublish(self)
        pro_publish_res = svc.do_publish()
        logger.info(pro_publish_res)
        if pro_publish_res.return_code == 0:
            pro_id = self.args.get("pro_id")
            data = self.get_pro_data(pro_id=pro_id)
            data.update(pro_publish_res=pro_publish_res)
            self.add_message(u"互联网发布信息添加成功！%s" % STATUS_PRO_TABLES.get(pro_publish_res.data.status).todo_value, level="success")
            tmpl = self.render_to_string("admin/guide/_step_3_publish_detail.html", **data)
            publish_notice_checker.delay(self.current_user.id)
            mail_title = u"%s申请的互联网信息添加成功！待受理" % (
                self.current_user.username or self.current_user.email,
            )
            mail_html = self.render_to_string("admin/mail/pro_publish.html", mail_title=mail_title, **data)
            sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        else:
            data = self.get_pro_data()
            data.update(pro_publish_res=pro_publish_res)
            tmpl = self.render_to_string("admin/guide/_step_3_publish.html", **data)
            self.add_message(u"互联网发布信息添加失败！(%s)(%s)" % (pro_publish_res.return_code, pro_publish_res.return_message), level="warning")
        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/publish/del", name="apply.publish.del", active="apply.publish")
class PublishDelHandler(ApplyHandler):
    u'删除互联网发布'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        id_list = self.get_arguments("id")
        svc = ApplyPublish(self, {"id_list": id_list})
        del_res = svc.do_del_pro_publish()
        logger.info(del_res)
        if del_res.return_code == 0:
            self.add_message(u"互联网发布信息删除成功！", level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"互联网发布信息删除失败！(%s)(%s)" % (del_res.return_code, del_res.return_message), level="warning")
        data = self.get_pro_data()
        svc = ApplyPublish(self, {"user_id": self.current_user.id})
        pro_publishs_res = svc.get_list()
        page = self.getPage(pro_publishs_res.data)
        data.update(page=page)
        tmpl = self.render_to_string("admin/apply/publish/index_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
