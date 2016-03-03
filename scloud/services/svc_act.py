# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.act import Act_History, Act_Pro_History
from scloud.models.project import Pro_Resource_Apply
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE


class ActHistoryService(BaseService):

    @thrownException
    def get_list(self):
        logger.info("------[get_profile]------")
        current_user = self.handler.current_user
        if current_user:
            history_list = self.db.query(
                Act_History
            ).filter(
                Act_History.user_id == current_user.id
            ).order_by(
                Act_History.id.desc()
            ).limit(10)

            # res = project.as_dict()
            # logger.info("project: %s" % res)
            return self.success(data=history_list)
        else:
            return NotFoundError()

    @thrownException
    def get_res_tasks(self):
        logger.info("------[get_res_tasks]------")
        current_user = self.handler.current_user
        if current_user:
            user_id = current_user.id
            role_ids = [role.id for role in current_user.user_roles]
            current_perms = current_user.current_perms
            conditions = and_()
            or_conditions = or_()
            # 如果是管理员用户，查看所有项目申请提交的任务状态
            # 如果是普通用户，查看自己资源审批的任务状态
            if "pro_resource_apply.view" in current_perms.keys():
                conditions.append(Pro_Resource_Apply.user_id == user_id)
            conditions.append(or_conditions)

            resource_list = self.db.query(
                Pro_Resource_Apply
            ).filter(
                conditions
            ).order_by(
                Pro_Resource_Apply.update_time.desc()
            )
            task_list = []
            for resource in resource_list:
                histories = resource.act_histories
                if len(histories) > 0:
                    last_history = histories[-1]
                    logger.info("#"*60)
                    logger.info(u"STATUS:%s(%s) - USER_ID:%s - CHECKER_ID:%s" % (last_history.status, STATUS_RESOURCE.get(last_history.status).value, last_history.user_id, last_history.checker_id))
                    logger.info("#"*60)
                    if "pro_resource_apply.check" in current_perms:
                         if last_history.status in [STATUS_RESOURCE.APPLIED,
                                                    STATUS_RESOURCE.PAYED, 
                                                    STATUS_RESOURCE.CONFIRMPAYED]:
                            task_list.append(last_history)
                    if "pro_resource_apply.view" in current_perms.keys():
                         if last_history.status in [STATUS_RESOURCE.REFUSED,
                                                    STATUS_RESOURCE.UNKNOWN,
                                                    STATUS_RESOURCE.REVOKED,
                                                    STATUS_RESOURCE.CHECKED,
                                                    STATUS_RESOURCE.CONFIRMPAYED]:
                            task_list.append(last_history)
            logger.info(task_list)
            return self.success(data=task_list)
        else:
            return NotFoundError()


    @thrownException
    def confirm_start_date(self):
        task_id = self.params.get("task_id")
        act = self.db.query(
            Act_Pro_History
        ).filter(
            Act_Pro_History.id == task_id
        ).first()
        if act:
            act.checker_id = self.handler.current_user.id
            self.db.add(act)
            return self.success()
        else:
            return NotFoundError()
