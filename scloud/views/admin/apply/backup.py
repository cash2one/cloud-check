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
from scloud.services.svc_apply_backups import ApplyBackups
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services.publish_task import publish_notice_checker
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.const import STATUS_PRO_TABLES
from .base import ApplyHandler


@url("/apply/backup/index", name="apply.backup", active="apply.backup")
class BackupIndexHandler(ApplyHandler):
    u'定期备份'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        data = self.get_pro_data()
        svc = ApplyBackups(self, {"user_id": self.current_user.id})
        pro_backups_res = svc.get_list()
        page = self.getPage(pro_backups_res.data)
        data.update(page=page)
        return self.render_to_string("admin/apply/backup/index.html", **data)


@url("/apply/backup/detail", name="apply.backup.detail", active="apply.backup")
class BackupDetailHandler(ApplyHandler):
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )
    u'定期备份详情'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ApplyBackups(self)
        pro_backup_res = svc.get_info()
        if pro_backup_res.return_code < 0:
            raise SystemError(pro_backup_res.return_code, pro_backup_res.return_message)
        logger.info(pro_backup_res)
        data = {
            "pro_backup_res": pro_backup_res,
        }
        return self.render_to_string("admin/apply/backup/detail.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/user/add", name="apply.user.add", active="apply.user.add")
@url("/apply/backup/add", name="apply.backup.add", active="apply.backup")
@url("/apply/backup/edit", name="apply.backup.edit", active="apply.backup")
class BackupAddHandler(ApplyHandler):
    u'定期备份申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        # pro_id = self.args.get("pro_id")
        # user_id = self.args.get("user_id", 0)
        data = self.get_pro_data()
        if self.kwargs["name"] == "apply.backup.edit":
            svc = ApplyBackups(self)
            # pro_users_res = svc.get_list()
            pro_backup_res = svc.get_info()
            data.update(pro_backup_res=pro_backup_res)
        return self.render_to_string("admin/apply/backup/add.html", **data)

    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ApplyBackups(self)
        pro_backup_res = svc.do_backups()
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        # svc = ApplyLoadBalance(self)
        # loadbalance_res = svc.get_loadbalance()
        # svc = ApplyBackups(self)
        # backups_res = svc.get_backups()
        data.update(pro_backup_res=pro_backup_res) # , loadbalance_res=loadbalance_res, backups_res=backups_res)
        logger.info(pro_backup_res)
        if pro_backup_res.return_code == 0:
            self.add_message(u"定期备份信息添加成功！%s" % STATUS_PRO_TABLES.get(pro_backup_res.data.status).todo_value, level="success")
            tmpl = self.render_to_string("admin/guide/_step_3_backup_detail.html", **data)
            publish_notice_checker.delay(self.current_user.id)
        else:
            tmpl = self.render_to_string("admin/guide/_step_3_backup.html", **data)
            self.add_message(u"定期备份信息添加失败！(%s)(%s)" % (pro_backup_res.return_code, pro_backup_res.return_message), level="warning")
        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/backup/del", name="apply.backup.del", active="apply.backup")
class BackupDelHandler(ApplyHandler):
    u'删除定期备份'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        id_list = self.get_arguments("id")
        svc = ApplyBackups(self, {"id_list": id_list})
        del_res = svc.do_del_pro_backup()
        logger.info(del_res)
        if del_res.return_code == 0:
            self.add_message(u"定期备份信息删除成功！", level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"定期备份信息删除失败！(%s)(%s)" % (del_res.return_code, del_res.return_message), level="warning")
        data = self.get_pro_data()
        svc = ApplyBackups(self, {"user_id": self.current_user.id})
        pro_backups_res = svc.get_list()
        page = self.getPage(pro_backups_res.data)
        data.update(page=page)
        tmpl = self.render_to_string("admin/apply/backup/index_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
