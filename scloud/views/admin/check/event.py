# -*- coding: utf-8 -*-

import scloud
from scloud.shortcuts import url
from scloud.config import logger
from scloud.const import pro_resource_apply_status_types
from scloud.handlers import Handler, AuthHandler
import requests
import urlparse
import urllib
import urllib2
import simplejson
import time
from tornado.web import asynchronous
from tornado import gen
from scloud.utils.permission import check_perms, GROUP
from scloud.services.svc_project import ProjectService
from scloud.services.svc_apply_publish import ApplyPublish
from scloud.services.svc_apply_balance import ApplyLoadBalance
from scloud.services.svc_apply_backups import ApplyBackups
from scloud.services.svc_apply_user import ProUserService
from scloud.services.svc_pro_resource_apply import ProResourceCheckService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.guide import GuideStepGetHandler
from scloud.const import STATUS_RESOURCE
from scloud.pubs.pub_tasks import TaskPublish


@url("/pro/pro_publish/(?P<id>\d+)/detail", name="pro_publish_detail", active="pro_table_check_list")
class ResourceCheckListHandler(AuthHandler):
    u'互联网发布申请内容明细'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        svc = ApplyPublish(self, {"id": kwargs["id"]})
        pro_publish_res = svc.get_publish()
        data = {
            "pro_publish_res": pro_publish_res
        }
        logger.info(pro_publish_res.data)
        return self.render_to_string("admin/check/_event_pro_publish_detail.html", **data)


@url("/pro/event/check_list", name="pro_table_check_list", active="pro_table_check_list")
class ResourceCheckListHandler(AuthHandler):
    u'待处理任务'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        pro_table = self.args.get("pro_table", "pro_user")
        pub_svc = TaskPublish(self)
        pub_data = pub_svc.publish_tasks(self.current_user.id, do_publish=False)
        data = pub_data.data
        _pro_table = data.get("%s_list" % pro_table, [])
        g = GROUP.get(pro_table)
        page = self.getPage(_pro_table)
        groups = []
        for keyword in ["pro_user", "pro_publish", "pro_balance", "pro_backup"]:
            groups.append(GROUP.get(keyword))
        logger.info(pub_data.data)
        return self.render_to_string("admin/check/event_list.html", g=g, groups=groups, page=page, pro_table=pro_table, pub_data=pub_data.data, **data)
