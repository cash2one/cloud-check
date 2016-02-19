# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.project import Pro_Info, Pro_Resource_Apply
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.async_services.svc_mail import sendMail
from scloud.async_services.svc_act import task_post_pro_res_apply_history
from scloud.const import admin_emails, STATUS_RESOURCE

mail_format = u"项目名[%(pro_name)s]-项目编号[%(pro_id)s]-%(user_name)s %(resource_status)s资源申请"

class ProResourceApplyService(BaseService):

    @thrownException
    def get_form_data(self):
        try:
            self.computer = int(self.params.get("computer", 0) or 0)
        except:
            return self.failure(ERROR.res_computer_invalid_err)
        try:
            self.cpu = int(self.params.get("cpu", 0) or 0)
        except:
            return self.failure(ERROR.res_cpu_invalid_err)
        try:
            self.memory = int(self.params.get("memory", 0) or 0)
        except:
            return self.failure(ERROR.res_memory_invalid_err)
        try:
            self.disk = int(self.params.get("disk", 0) or 0)
        except:
            return self.failure(ERROR.res_disk_invalid_err)
        try:
            self.disk_backup = int(self.params.get("disk_backup", 0) or 0)
        except:
            return self.failure(ERROR.res_disk_backup_invalid_err)
        try:
            self.out_ip = int(self.params.get("out_ip", 0) or 0)
        except:
            return self.failure(ERROR.res_out_ip_invalid_err)
        try:
            self.snapshot = int(self.params.get("snapshot", 0) or 0)
        except:
            return self.failure(ERROR.res_snapshot_invalid_err)
        try:
            self.loadbalance = int(self.params.get("loadbalance", 0) or 0)
        except:
            return self.failure(ERROR.res_loadbalance_invalid_err)
        try:
            self.internet_ip = int(self.params.get("internet_ip", -1) or -1)
        except:
            return self.failure(ERROR.res_internet_ip_invalid_err)
        try:
            self.internet_ip_ssl = int(self.params.get("internet_ip_ssl", -1) or -1)
        except:
            return self.failure(ERROR.res_internet_ip_ssl_invalid_err)
        try:
            self.period = int(self.params.get("period", 0) or 0)
        except:
            return self.failure(ERROR.res_period_invalid_err)
        try:
            start_date = self.params.get("start_date", "")
            if start_date == "":
                self.start_date = ""
            else:
                self.start_date = datetime.strptime(self.params.get("start_date"), "%Y-%m-%d")
        except:
            return self.failure(ERROR.res_start_date_invalid_err)
        try:
            self.unit_fee = "{:,.2f}".format(float(self.params.get("unit_fee") or 0))
        except:
            return self.failure(ERROR.res_unit_fee_invalid_err)
        try:
            self.total_fee = "{:,.2f}".format(float(self.params.get("total_fee") or 0))
        except:
            return self.failure(ERROR.res_total_fee_invalid_err)
        return True

    @thrownException
    def generate_fee(self):
        logger.info("------[generate_fee]------")
        self.get_form_data()
        if self.period == 0:
            return self.failure(ERROR.res_period_empty_err)
        unit_fee = 10
        total_fee = 100
        data = {
            "unit_fee": unit_fee,
            "total_fee": total_fee
        }
        return self.success(data=data)

    @thrownException
    def do_apply(self):
        form_res = self.get_form_data()
        pro_id = self.params.get("pro_id")
        user_id = self.params.get("user_id")
        if not pro_id:
            return self.failure(ERROR.not_found_err)
        if not user_id:
            return self.failure(ERROR.user_empty_err)
        if isinstance(form_res, dict):
            return form_res
        if self.computer == 0:
            return self.failure(ERROR.res_computer_empty_err)
        if self.cpu == 0:
            return self.failure(ERROR.res_cpu_empty_err)
        if self.memory == 0:
            return self.failure(ERROR.res_memory_empty_err)
        if self.disk == 0:
            return self.failure(ERROR.res_disk_empty_err)
        if self.disk_backup == 0:
            return self.failure(ERROR.res_disk_backup_empty_err)
        if self.out_ip == 0:
            return self.failure(ERROR.res_out_ip_empty_err)
        if self.snapshot == 0:
            return self.failure(ERROR.res_snapshot_empty_err)
        if self.loadbalance == 0:
            return self.failure(ERROR.res_loadbalance_empty_err)
        if self.internet_ip == -1:
            logger.info(self.internet_ip)
            return self.failure(ERROR.res_internet_ip_empty_err)
        if self.internet_ip_ssl == -1:
            return self.failure(ERROR.res_internet_ip_ssl_invalid_err)
        if self.period == 0:
            return self.failure(ERROR.res_period_empty_err)
        if self.computer == 0:
            return self.failure(ERROR.res_computer_empty_err)
        if self.computer == 0:
            return self.failure(ERROR.res_computer_empty_err)
        if self.computer == 0:
            return self.failure(ERROR.res_computer_empty_err)
        pro_info = self.db.query(
            Pro_Info
        ).filter(
            Pro_Info.pro_id == pro_id
        ).first()
        applies = pro_info.pro_resource_applies
        if len(applies) > 0:
            first_apply = applies[0]
            last_apply = applies[-1]
            if last_apply.status >= 0:
                return self.failure(ERROR.res_new_apply_err)
        else:
            first_apply = None
            last_apply = None
        apply = Pro_Resource_Apply()
        apply.pro_id = pro_id
        apply.computer = self.computer
        apply.cpu = self.cpu
        apply.memory = self.memory
        apply.disk = self.disk
        apply.disk_backup = self.disk_backup
        apply.out_ip = self.out_ip
        apply.snapshot = self.snapshot
        apply.loadbalance = self.loadbalance
        apply.internet_ip = self.internet_ip
        apply.internet_ip_ssl = self.internet_ip_ssl
        apply.start_date = self.start_date
        apply.period = self.period
        apply.unit_fee = self.unit_fee
        apply.total_fee = self.total_fee
        apply.user_id = user_id
        if first_apply:
            apply.desc = u'资源调整'
        self.db.add(apply)
        self.db.flush()
        html = self.render_to_string("admin/mail/pro_info.html", resource_apply=apply)
        logger.info("<"+"="*60+">")
        logger.info(html)
        user_name = apply.user.email or apply.user.mobile
        mail_title = u"项目名[%s]-项目编号[%s]-%s已提交资源申请".encode("utf-8") % (apply.project.name, apply.pro_id, user_name)
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, html)
        task_post_pro_res_apply_history.delay(status=apply.status, content=apply.desc, pro_id=pro_id, res_apply_id=apply.id, user_id=user_id)
        return self.success(data=apply)

    @thrownException
    def do_revoke(self):
        res_id = self.params.get("res_id", 0)
        user_id = self.params.get("user_id", 0)
        resource = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
        if not resource:
            return self.failure(ERROR.not_found_err)
        if resource.status != 0:
            return self.failure(ERROR.res_revoke_err)
        resource.status = STATUS_RESOURCE.REVOKED
        self.db.add(resource)
        self.db.flush()
        mail_title = mail_format % {
            "pro_name": resource.project.name,
            "pro_id": resource.project.id,
            "user_name": resource.user.email or resource.user.mobile,
            "resource_status": STATUS_RESOURCE.revoked.value
        }
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_title)
        task_post_pro_res_apply_history.delay(status=resource.status, content=mail_title, pro_id=resource.project.id, res_apply_id=resource.id, user_id=user_id)
        return self.success(data=resource)
