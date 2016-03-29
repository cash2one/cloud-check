# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types
from scloud.models.project import Pro_Info, Pro_Backup 
import simplejson

class ApplyBackups(BaseService):

    @thrownException
    def get_backups(self):
        pro_id = self.params.get("pro_id")
        pro_info = self.db.query(
             Pro_Info
        ).filter(
            Pro_Info.id == pro_id
        ).first()
        applies = pro_info.pro_resource_applies
        last_apply = applies[-1]
        backups_plot = last_apply.backups_plot
        return self.success(data=backups_plot)

    @thrownException
    def do_backups(self):
        pro_id = self.params.get("pro_id")
        res_apply_id = self.params.get("res_apply_id")
        plot_str = self.params.get("backups", "")
        plot_s = simplejson.loads(plot_str) 
        for plot_mem in plot_s:
            disk = plot_mem['disk']
            plot = plot_mem['plot']
            interval = plot_mem['interval']
            backup_time = plot_mem['backup_time']
            if not disk:
                return self.failure(ERROR.pro_backups_disk_empty_err)
            if not plot:
                return self.failure(ERROR.pro_backups_plot_empty_err)
            if plot in [u"月", u"周"] and not interval:
                return self.failure(ERROR.pro_backups_interval_empty_err)
            if not backup_time:
                return self.failure(ERROR.pro_backups_backup_time_empty_err)
        do_backups_info, created = Pro_Backup.get_or_create_obj(self.db, pro_id=pro_id)
        do_backups_info.pro_id = pro_id
        do_backups_info.res_apply_id = res_apply_id
        do_backups_info.plot = plot_str
        self.db.add(do_backups_info)
        self.db.flush()
        return self.success(data=do_backups_info)

