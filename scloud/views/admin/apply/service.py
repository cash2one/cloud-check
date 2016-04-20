# -*- coding: utf-8 -*-

import scloud
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE, STATUS_PRO_TABLES
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
from scloud.services.svc_apply_balance import ApplyLoadBalance
from scloud.services.svc_apply_backups import ApplyBackups
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services.publish_task import publish_notice_checker
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from .base import ApplyHandler


@url("/apply/service/index", name="apply.service", active="apply.service")
class GuideHandler(ApplyHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        data = self.get_pro_data()
        return self.render_to_string("admin/apply/service/index.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/service/add", name="apply.service.add", active="apply.service.add")
@url("/apply/service/add", name="apply.service.add", active="apply.service.add")
class GuideHandler(ApplyHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        svc = ApplyPublish(self)
        publish_res = svc.get_publish()
        svc = ApplyLoadBalance(self)
        loadbalance_res = svc.get_loadbalance()
        svc = ApplyBackups(self)
        backups_res = svc.get_backups()
        data.update(publish_res=publish_res,
                    loadbalance_res=loadbalance_res,
                    backups_res=backups_res)
        backups = backups_res.data
        logger.info(backups)
        # if backups:
        #     logger.info(backups.plot)
        # else:
        #     logger.info("[]")
        # pro_info_res = data["pro_info_res"]
        # applies = pro_info_res.data.pro_resource_applies
        # logger.info(len(applies))
        # last_apply = applies[-1]
        # logger.info(last_apply.as_dict())
        return self.render_to_string("admin/apply/service/add.html", **data)


@url("/apply/service/publish/add", name="apply.service.publish.add", active="apply.service.add")
class GuideHandler(ApplyHandler):
    u'互联网发布申请'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ApplyPublish(self)
        pro_publish_res = svc.do_publish()
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        # svc = ApplyLoadBalance(self)
        # loadbalance_res = svc.get_loadbalance()
        # svc = ApplyBackups(self)
        # backups_res = svc.get_backups()
        data.update(pro_publish_res=pro_publish_res) # , loadbalance_res=loadbalance_res, backups_res=backups_res)
        logger.info(pro_publish_res)
        if pro_publish_res.return_code == 0:
            self.add_message(u"互联网发布信息添加成功！%s" % STATUS_PRO_TABLES.get(pro_publish_res.data.status).todo_value, level="success")
            tmpl = self.render_to_string("admin/guide/_step_3_publish_detail.html", **data)
            publish_notice_checker.delay(self.current_user.id)
        else:
            tmpl = self.render_to_string("admin/guide/_step_3_publish.html", **data)
            self.add_message(u"互联网发布信息添加失败！(%s)(%s)" % (pro_publish_res.return_code, pro_publish_res.return_message), level="warning")
        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/service/loadbalance/add", name="apply.service.loadbalance.add", active="apply.service.add")
class GuideHandler(ApplyHandler):
    u'负载均衡申请'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ApplyLoadBalance(self)
        loadbalance_res = svc.do_loadbalance()
        if loadbalance_res.return_code == 0:
            self.add_message(u"负载均衡申请成功！%s" % STATUS_PRO_TABLES.get(loadbalance_res.data.status).todo_value, level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"负载均衡申请失败！(%s)(%s)" % (loadbalance_res.return_code, loadbalance_res.return_message), level="warning")
        svc = ApplyPublish(self)
        publish_res = svc.get_publish()
        svc = ApplyBackups(self)
        backups_res = svc.get_backups()
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        data.update(loadbalance_res=loadbalance_res, backups_res=backups_res, publish_res=publish_res)
        logger.info(loadbalance_res)
        tmpl = self.render_to_string("admin/apply/service/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/apply/service/backups/add", name="apply.service.backups.add", active="apply.service.add")
class GuideHandler(ApplyHandler):
    u'定期备份申请'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ApplyBackups(self)
        backups_res = svc.do_backups()
        if backups_res.return_code == 0:
            self.add_message(u"定期备份申请成功！%s" % STATUS_PRO_TABLES.get(backups_res.data.status).todo_value, level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"定期备份申请失败！(%s)(%s)" % (backups_res.return_code, backups_res.return_message), level="warning")
        pro_id = self.args.get("pro_id")
        svc = ApplyLoadBalance(self)
        loadbalance_res = svc.get_loadbalance()
        data = self.get_pro_data(pro_id=pro_id)
        data.update(backups_res=backups_res, loadbalance_res=loadbalance_res)
        logger.info(backups_res)
        tmpl = self.render_to_string("admin/apply/service/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))

