# -*- coding: utf-8 -*-

import scloud
from scloud.shortcuts import url
from scloud.config import logger
# from scloud.const import pro_resource_apply_status_types
from scloud.handlers import AuthHandler
# import requests
# import urlparse
# import urllib
# import urllib2
import simplejson
# import time
# from tornado.web import asynchronous
# from tornado import gen
from scloud.utils.permission import check_perms, GROUP
from scloud.services.svc_project import ProjectService
from scloud.services.svc_apply_publish import ApplyPublish
from scloud.services.svc_apply_balance import ApplyLoadBalance
from scloud.services.svc_apply_backups import ApplyBackups
from scloud.services.svc_apply_user import ProUserService
from scloud.services.svc_pro_event import EventService
from scloud.services.svc_apply_check import ApplyCheckService
# from scloud.services.svc_pro_resource_apply import ProResourceCheckService
# from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
# from scloud.utils.error import SystemError
# from scloud.views.admin.guide import GuideStepGetHandler
from scloud.const import STATUS_PRO_TABLES
from scloud.pubs.pub_tasks import TaskPublish
from scloud.async_services.publish_task import publish_notice_user, publish_tasks


@url("/pro/event/check_list", name="pro_table_check_list", active="pro_table_check_list")
class EventCheckListHandler(AuthHandler):
    u'待处理任务'
    def get_index_page(self, pro_table):
        pub_svc = TaskPublish(self, {"pro_table": pro_table})
        pub_data = pub_svc.publish_tasks(self.current_user.id, do_publish=False)
        data = pub_data.data
        _pro_table = data.get("%s_list" % pro_table, [])
        g = GROUP.get(pro_table)
        page = self.getPage(_pro_table)
        groups = []
        for keyword in ["pro_user", "pro_publish", "pro_balance", "pro_backup", "pro_event"]:
            groups.append(GROUP.get(keyword))
        # logger.info(pub_data.data)
        data.update(
            g=g,
            groups=groups,
            page=page,
            pro_table=pro_table,
            pub_data=pub_data.data
        )
        return data

    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self):
        pro_table = self.args.get("pro_table", "pro_user")
        data = self.get_index_page(pro_table)
        return self.render_to_string("admin/check/event_list.html", **data)


@url("/pro/pro_publish/(?P<id>\d+)/detail", name="pro_publish_detail", active="pro_table_check_list")
class ProPublishDetailHandler(AuthHandler):
    u'互联网发布申请内容明细'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        svc = ApplyPublish(self, {"id": kwargs["id"]})
        pro_publish_res = svc.get_publish()
        data = {
            "pro_publish_res": pro_publish_res,
            "pro_table": "pro_publish",
        }
        # logger.info(pro_publish_res.data)
        return self.render_to_string("admin/check/_event_pro_publish_detail.html", **data)


@url("/pro/(?P<pro_id>\d+)/pro_user/detail", name="pro_users_detail", active="pro_table_check_list")
class ProUsersDetailHandler(AuthHandler):
    u'互联网发布申请内容明细'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        svc = ProUserService(self, {"pro_id": kwargs["pro_id"]})
        pro_users_res = svc.get_list()
        data = {
            "pro_users_res": pro_users_res,
            "pro_table": "pro_user",
        }
        # logger.info(pro_users_res.data)
        return self.render_to_string("admin/check/_event_pro_user_detail.html", **data)


@url("/pro/pro_balance/(?P<id>\d+)/detail", name="pro_balance_detail", active="pro_table_check_list")
class ProBalanceDetailHandler(AuthHandler):
    u'互联网发布申请内容明细'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        svc = ApplyLoadBalance(self, {"id": kwargs["id"]})
        pro_balance_res = svc.get_info()
        data = {
            "pro_balance_res": pro_balance_res,
            "pro_table": "pro_balance",
        }
        # logger.info(pro_balance_res.data)
        return self.render_to_string("admin/check/_event_pro_balance_detail.html", **data)


@url("/pro/pro_backup/(?P<id>\d+)/detail", name="pro_backup_detail", active="pro_table_check_list")
class ProBackupDetailHandler(AuthHandler):
    u'互联网发布申请内容明细'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        svc = ApplyBackups(self, {"id": kwargs["id"]})
        pro_backup_res = svc.get_info()
        data = {
            "pro_backup_res": pro_backup_res,
            "pro_table": "pro_backup",
        }
        # logger.info(pro_backup_res.data)
        return self.render_to_string("admin/check/_event_pro_backup_detail.html", **data)


@url("/pro/pro_event/(?P<id>\d+)/detail", name="pro_event_detail", active="pro_table_check_list")
class ProEventDetailHandler(AuthHandler):
    u'互联网发布申请内容明细'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        svc = EventService(self, {"id": kwargs["id"]})
        pro_event_res = svc.get_info()
        data = {
            "pro_event_res": pro_event_res,
            "pro_table": "pro_event",
        }
        # logger.info(pro_event_res.data)
        return self.render_to_string("admin/check/_event_pro_event_detail.html", **data)


@url("/pro/pro_table/do_check", name="pro_table_do_check")
class ProTableDoCheckHandler(EventCheckListHandler):
    u'''受理通过'''

    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("DO_CHECK",)

    @check_perms('pro_resource_apply.check')
    @unblock
    def do_check(self):
        pro_table = ApplyCheckService(self)
        check_res = pro_table.do_check()
        return self.do_return(check_res)

    def do_return(self, check_res):
        pro_table = self.args.get("pro_table")
        doc = GROUP.get(pro_table).name
        # logger.info(doc)
        if check_res.return_code == 0:
            self.add_message(u"所选申请%s已处理完毕" % doc, level="success")
            pro_users = check_res.data
            users = [u.user_id for u in pro_users]
            for user_id in set(users):
                publish_notice_user.delay(user_id)
        if pro_table == "pro_event":
            ids = self.args.get("ids")
            id_list = [int(i) for i in ids.split(",") if i.strip().isdigit()]
            for id in id_list:
                svc = EventService(self, {"id": id, "reply_content": STATUS_PRO_TABLES.checked.value, "status": STATUS_PRO_TABLES.CHECKED})
                svc.do_reply()
        data = self.get_index_page(pro_table)
        tmpl = self.render_to_string("admin/check/event_list_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/pro/pro_table/do_confirm", name="pro_table_do_confirm")
class ProTableDoConfirmHandler(AuthHandler):
    u'''确认结果'''

    @check_perms('pro_resource_apply.view')
    @unblock
    def post(self):
        pro_table = ApplyCheckService(self)
        confirm_res = pro_table.do_confirm()
        # logger.info(confirm_res)
        publish_tasks.delay(self.current_user.id)
        return simplejson.dumps(self.success(data=confirm_res))
