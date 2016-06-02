# -*- coding: utf-8 -*-

import simplejson
# from datetime import datetime
# from tornado import gen
from scloud.services.base import BaseService
from scloud.services.svc_pt_user import PtUserService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
# from scloud.models.act import Act_History, Act_Pro_History
# from scloud.models.project import Pro_Resource_Apply
from scloud.config import logger, thrownException
# from sqlalchemy import and_, or_
# from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError

from scloud.services.svc_act import ActHistoryService
from scloud.services.svc_apply_user import ProUserService
from scloud.services.svc_apply_publish import ApplyPublish
from scloud.services.svc_apply_balance import ApplyLoadBalance
from scloud.services.svc_apply_backups import ApplyBackups
from scloud.services.svc_pro_event import EventService
from scloud.const import STATUS_RESOURCE, STATUS_PRO_TABLES
from scloud.shortcuts import render_to_string
from scloud.pubs.base import r


class TaskPublish(BaseService):

    @thrownException
    def publish_tasks(self, user_id, pro_id=None, action="on_task", do_publish=True):
        logger.info("------[publish_tasks]------")

        user_svc = PtUserService(self, {"user_id": user_id, "pro_id": pro_id})
        pt_user_res = user_svc.get_info()
        logger.info(pt_user_res)
        if "pro_resource_apply.check" in pt_user_res.data.get_current_perms():
            imchecker = True
        else:
            imchecker = False
        # 获取任务列表
        svc = ActHistoryService(self, {"user_id": user_id, "pro_id": pro_id})
        tasks_res = svc.get_res_tasks()
        data = {
            "tasks_res": tasks_res,
            "task_list": tasks_res.data,
            "imchecker": imchecker,
            "STATUS_RESOURCE": STATUS_RESOURCE
        }

        # 获取用户申请列表
        svc = ProUserService(self, {"user_id": user_id, "pro_id": pro_id})
        pro_user_list_res = svc.get_list()
        if imchecker:
            pro_user_list = [i for i in pro_user_list_res.data[::-1] if i.status == STATUS_PRO_TABLES.APPLIED]
        else:
            pro_user_list = [i for i in pro_user_list_res.data[::-1] if i.status in [STATUS_PRO_TABLES.REFUSED, STATUS_PRO_TABLES.CHECKED]]
        data.update({
            "pro_user_list": pro_user_list,
            "imchecker": imchecker,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES
        })
        # logger.info(pro_user_list)

        # 获取互联网发布申请列表
        svc = ApplyPublish(self, {"user_id": user_id, "pro_id": pro_id})
        pro_publish_list_res = svc.get_list()
        # logger.info(pro_publish_list_res.data)
        if imchecker:
            pro_publish_list = [i for i in pro_publish_list_res.data[::-1] if i.status == STATUS_PRO_TABLES.APPLIED]
        else:
            pro_publish_list = [i for i in pro_publish_list_res.data[::-1] if i.status in [STATUS_PRO_TABLES.REFUSED, STATUS_PRO_TABLES.CHECKED]]
        data.update({
            "pro_publish_list": pro_publish_list,
            "imchecker": imchecker,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES
        })

        # 获取负载均衡申请列表
        svc = ApplyLoadBalance(self, {"user_id": user_id, "pro_id": pro_id})
        pro_balance_list_res = svc.get_list()
        # logger.info(pro_balance_list_res.data)
        if imchecker:
            pro_balance_list = [i for i in pro_balance_list_res.data[::-1] if i.status == STATUS_PRO_TABLES.APPLIED]
        else:
            pro_balance_list = [i for i in pro_balance_list_res.data[::-1] if i.status in [STATUS_PRO_TABLES.REFUSED, STATUS_PRO_TABLES.CHECKED]]
        data.update({
            "pro_balance_list": pro_balance_list,
            "imchecker": imchecker,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES
        })

        # 获取定期备份申请列表
        svc = ApplyBackups(self, {"user_id": user_id, "pro_id": pro_id})
        pro_backup_list_res = svc.get_list()
        # logger.info(pro_backup_list_res.data)
        if imchecker:
            pro_backup_list = [i for i in pro_backup_list_res.data[::-1] if i.status == STATUS_PRO_TABLES.APPLIED]
        else:
            pro_backup_list = [i for i in pro_backup_list_res.data[::-1] if i.status in [STATUS_PRO_TABLES.REFUSED, STATUS_PRO_TABLES.CHECKED]]
        data.update({
            "pro_backup_list": pro_backup_list,
            "imchecker": imchecker,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES
        })

        # 获取定期备份申请列表
        svc = EventService(self, {"user_id": user_id, "pro_id": pro_id})
        pro_event_list_res = svc.get_list()
        # logger.info(pro_event_list_res.data)
        if imchecker:
            pro_event_list = [i for i in pro_event_list_res.data[::-1] if i.status == STATUS_PRO_TABLES.APPLIED]
        else:
            pro_event_list = [i for i in pro_event_list_res.data[::-1] if i.status in [STATUS_PRO_TABLES.REFUSED, STATUS_PRO_TABLES.CHECKED]]
        data.update({
            "pro_event_list": pro_event_list,
            "imchecker": imchecker,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES
        })

        # 获取任务列表总和
        pro_tables_total = len(pro_user_list) + len(pro_publish_list) + len(pro_balance_list) + len(pro_backup_list) + len(pro_event_list)
        logger.info("len(pro_user_list): %s" % len(pro_user_list))
        logger.info("len(pro_publish_list): %s" % len(pro_publish_list))
        logger.info("len(pro_balance_list): %s" % len(pro_balance_list))
        logger.info("len(pro_backup_list): %s" % len(pro_backup_list))
        logger.info("len(pro_event_list): %s" % len(pro_event_list))
        data["pro_tables_total"] = pro_tables_total
        data["tasks_total"] = len(tasks_res.data)
        logger.info("total: %s" % pro_tables_total)
        logger.info("tasks_total: %s" % len(tasks_res.data))
        if do_publish:
            self.do_publish(user_id, action, **data)
        return self.success(data=data)

    @thrownException
    def do_publish(self, user_id, action, template="admin/notice/tasks.html", **data):
        logger.info("[ %s: %s ]" % (action, user_id))
        chat = {
            "user_id": user_id,
            "action": action,

            "pro_user_num": len(data["pro_user_list"]),
            "pro_publish_num": len(data["pro_publish_list"]),
            "pro_balance_num": len(data["pro_balance_list"]),
            "pro_backup_num": len(data["pro_backup_list"]),
            "pro_event_num": len(data["pro_event_list"]),
            "tasks_total": data["tasks_total"],
            "pro_tables_total": data["pro_tables_total"],
            # "html": render_to_string(template, **data),
            "tmpl_tasks": render_to_string("admin/notice/tasks.html", **data),
            "tmpl_pro_tables": render_to_string("admin/notice/pro_tables.html", **data)
        }
        # from scloud.app import reverse_url
        # html = request.get(reverse_url("callback_%s" % template))

        logger.info(template)
        r.publish("test_realtime", simplejson.dumps(chat))
        return True
