# -*- coding: utf-8 -*-

from datetime import datetime
# from tornado import gen
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
# from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.const import STATUS_PRO_TABLES
from scloud.models.project import (Pro_User, Pro_Publish, Pro_Balance, Pro_Backup, Pro_Event)


class ApplyCheckService(BaseService):
    pro_tables = {
        "pro_user": Pro_User,
        "pro_publish": Pro_Publish,
        "pro_balance": Pro_Balance,
        "pro_backup": Pro_Backup,
        "pro_event": Pro_Event,
    }

    @thrownException
    def do_check(self):
        pro_table = self.params.get("pro_table")
        action = self.params.get("action")
        reason = self.params.get("reason")
        actions = [STATUS_PRO_TABLES.get(i).value_en for i in STATUS_PRO_TABLES.keys() if isinstance(i, int)]
        if action not in actions:
            return self.failure(ERROR.res_do_resource_action_err)
        ProTable = self.pro_tables.get(pro_table)
        if not ProTable:
            return self.failure(ERROR.not_found_err)
        ids = self.params.get("ids")
        id_list = [int(i) for i in ids.split(",") if i.strip().isdigit()]
        logger.info(id_list)
        pro_table_objs = []
        for id in id_list:
            pro_table_obj = self.db.query(
                ProTable
            ).filter(
                ProTable.id == id
            ).first()
            if pro_table_obj:
                if action == STATUS_PRO_TABLES.checked.value_en:
                    pro_table_obj.status = STATUS_PRO_TABLES.CHECKED
                    pro_table_obj.reason = u''
                elif action == STATUS_PRO_TABLES.refused.value_en:
                    pro_table_obj.status = STATUS_PRO_TABLES.REFUSED
                    pro_table_obj.reason = reason
                pro_table_obj.checker_id = self.handler.current_user.id
                pro_table_obj.check_time = datetime.now()
                self.db.add(pro_table_obj)
                self.db.flush()
                pro_table_objs.append(pro_table_obj)
        return self.success(data=pro_table_objs)

    @thrownException
    def do_confirm(self):
        pro_table = self.params.get("pro_table")
        ProTable = self.pro_tables.get(pro_table)
        if not ProTable:
            return self.failure(ERROR.not_found_err)
        ids = self.params.get("ids")
        id_list = [int(i) for i in ids.split(",") if i.strip().isdigit()]
        logger.info(id_list)
        # pro_table_objs = []
        for id in id_list:
            pro_table_obj = self.db.query(
                ProTable
            ).filter(
                ProTable.id == id
            ).first()
            if pro_table_obj:
                pro_table_obj.status = STATUS_PRO_TABLES.CONFIRMED
                pro_table_obj.checker_id = self.handler.current_user.id
                pro_table_obj.check_time = datetime.now()
                self.db.add(pro_table_obj)
                self.db.flush()
                logger.info(pro_table_obj)
                # pro_table_objs.append(pro_table_obj)
        return self.success(data=id_list)
