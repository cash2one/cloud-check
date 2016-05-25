# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from tornado.util import ObjectDict
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.project import Pro_Info, Pro_Resource_Apply
from scloud.models.environment import Env_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from sqlalchemy import func
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.async_services.svc_mail import sendMail
from scloud.async_services.svc_act import task_post_pro_res_apply_history
from scloud.async_services.publish_task import publish_notice_user
from scloud.const import admin_emails, STATUS_RESOURCE
from scloud.models.environment import Env_Resource_Fee
from voluptuous import (Schema, Required, Error,
    Invalid, ALLOW_EXTRA, MultipleInvalid, TypeInvalid, ValueInvalid,
    All, Length, Range)

mail_format = u"项目名[%(pro_name)s]-项目编号[%(pro_id)s]-%(user_name)s %(resource_status)s资源申请"

mail_title_format = u"%(user_name)s %(action)s[%(pro_name)s-%(res_desc)s]%(todo_action)s"


class ProResourceApplyService(BaseService):

    def validate_pro_info(self, value):
        if str(value).strip() == '':
            value = 0
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                raise Invalid(u"必须为数字")
        if value <= 0:
            raise Invalid(ERROR.pro_id_empty_err.errvalue)
        return value

    def validate_num(self, value):
        if str(value).strip() == '':
            value = 0
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                raise Invalid(u"必须为数字")
        if value < 0:
            raise ValueInvalid(u'必须为大于等于0的数字')
        return value

    def validate_num_more_than_1(self, value):
        if str(value).strip() == '':
            value = 0
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                raise Invalid(u"必须为数字")
        if value <= 0:
            raise ValueInvalid(u'必须为大于等于0的数字')
        return value

    def get_param_schema(self):
        param_schema = Schema({
            "pro_id": self.validate_pro_info,
            "computer": self.validate_num_more_than_1,
            "cpu": self.validate_num_more_than_1,
            "memory": self.validate_num_more_than_1,
            'disk': self.validate_num,
            'disk_amount': self.validate_num,
            'disk_backup': self.validate_num,
            'disk_backup_amount': self.validate_num,
            'out_ip': self.validate_num,
            'snapshot': self.validate_num,
            'loadbalance': self.validate_num,
            'internet_ip': self.validate_num,
            'bandwidth': self.validate_num,
            'internet_ip_ssl': self.validate_num,
            'period': self.validate_num_more_than_1,
        }, extra=ALLOW_EXTRA)
        return param_schema

    @thrownException
    def get_list(self):
        search = self.params.get("search")
        status = self.params.get("status")
        conditions = and_()
        conditions.append(Pro_Resource_Apply.is_enable == 1)
        conditions.append(Pro_Resource_Apply.user_id == self.handler.current_user.id)
        if search:
            conditions.append(Pro_Info.name.like('%' + search + '%'))
        if status:
            conditions.append(Pro_Resource_Apply.status == status)
        resources_res = self.db.query(
            Pro_Resource_Apply
        ).join(
            Pro_Info, Pro_Resource_Apply.pro_id == Pro_Info.id
        ).filter(
            conditions
        ).order_by(Pro_Resource_Apply.id.desc()).all()
        return self.success(data=resources_res)

    @thrownException
    def get_resource(self):
        res_id = self.params.get("res_id", 0)
        res_apply_id = self.params.get("res_apply_id", 0)
        if not res_id:
            res_id = res_apply_id
        resource_res = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
        if not resource_res:
            return self.failure(ERROR.not_found_err)
        return self.success(data=resource_res)

    @thrownException
    def check_form_valid(self, param_schema):
        try:
            check_result = param_schema(self.params)
            logger.info(check_result)
            return self.success(check_result)
        except MultipleInvalid as e:
            logger.error(u"\t %s" % e.errors)
            ziped_errors = [(i.path[0], i) for i in e.errors]
            messages = []
            for path, err in ziped_errors:
                if hasattr(ERROR, "res_%s_invalid_err" % path):
                    column = getattr(Pro_Resource_Apply, path)
                    column_info = column.info["name"]
                    msg = "%s %s" % (getattr(ERROR, "res_%s_invalid_err" % path).errvalue, "'%s'%s" % (column_info, err.msg))
                else:
                    msg = err.msg
                messages.append(msg)
                # messages.append("%s %s" % (self.failure(getattr(ERROR, "res_%s_invalid_err" % path)).return_message, "'%s'%s" % (path, err.msg)))
            # raise Exception(u"{}".format(",".join(messages)))
            return self.failures(messages)

    # @thrownException
    # def check_form_valid(self):
    #     try:
    #         self.computer = int(self.params.get("computer", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_computer_invalid_err)
    #     try:
    #         self.cpu = int(self.params.get("cpu", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_cpu_invalid_err)
    #     try:
    #         self.memory = int(self.params.get("memory", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_memory_invalid_err)
    #     try:
    #         self.disk = int(self.params.get("disk", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_disk_invalid_err)
    #     try:
    #         self.disk_backup = int(self.params.get("disk_backup", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_disk_backup_invalid_err)
    #     try:
    #         self.out_ip = int(self.params.get("out_ip", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_out_ip_invalid_err)
    #     try:
    #         self.snapshot = int(self.params.get("snapshot", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_snapshot_invalid_err)
    #     try:
    #         self.loadbalance = int(self.params.get("loadbalance", 0) or 0)
    #     except:
    #         return self.failure(ERROR.res_loadbalance_invalid_err)
    #     try:
    #         self.internet_ip = int(self.params.get("internet_ip", -1) or -1)
    #     except:
    #         return self.failure(ERROR.res_internet_ip_invalid_err)
    #     try:
    #         self.internet_ip_ssl = int(self.params.get("internet_ip_ssl", -1) or -1)
    #     except:
    #         return self.failure(ERROR.res_internet_ip_ssl_invalid_err)
    #     try:
    #         if self.params.get("period", "").strip() == "":
    #             return self.failure(ERROR.res_period_empty_err)
    #         self.period = int(self.params.get("period"))
    #     except:
    #         return self.failure(ERROR.res_period_invalid_err)
    #     try:
    #         start_date = self.params.get("start_date", "")
    #         if start_date == "":
    #             self.start_date = ""
    #         else:
    #             self.start_date = datetime.strptime(self.params.get("start_date"), "%Y-%m-%d %H:%M:%S")
    #     except:
    #         return self.failure(ERROR.res_start_date_invalid_err)
    #     try:
    #         self.unit_fee = "{:,.2f}".format(float(self.params.get("unit_fee") or 0))
    #     except:
    #         return self.failure(ERROR.res_unit_fee_invalid_err)
    #     try:
    #         self.total_fee = "{:,.2f}".format(float(self.params.get("total_fee") or 0))
    #     except:
    #         return self.failure(ERROR.res_total_fee_invalid_err)
    #     return self.success()

    def check_form_empty(self):
        if self.computer == 0:
            return self.failure(ERROR.res_computer_empty_err)
        if self.cpu == 0:
            return self.failure(ERROR.res_cpu_empty_err)
        if self.memory == 0:
            return self.failure(ERROR.res_memory_empty_err)
        if self.disk == 0:
            return self.failure(ERROR.res_disk_empty_err)
        if self.disk_amount == 0:
            return self.failure(ERROR.res_disk_amount_empty_err)
        # if self.disk_backup == 0:
        #     return self.failure(ERROR.res_disk_backup_empty_err)
        if self.disk_backup_amount == 0:
            return self.failure(ERROR.res_disk_backup_amount_empty_err)
        if self.out_ip == 0:
            return self.failure(ERROR.res_out_ip_empty_err)
        if self.snapshot == 0:
            return self.failure(ERROR.res_snapshot_empty_err)
        if self.loadbalance == 0:
            return self.failure(ERROR.res_loadbalance_empty_err)
        if self.internet_ip == -1:
            logger.info(self.internet_ip)
            return self.failure(ERROR.res_internet_ip_empty_err)
        # if self.bandwidth == -1:
        #     logger.info(self.bandwidth)
        #     return self.failure(ERROR.res_bandwidth_empty_err)
        # if self.internet_ip_ssl == -1:
        #     return self.failure(ERROR.res_internet_ip_ssl_invalid_err)
        if self.params.get('period') == 0:
            return self.failure(ERROR.res_period_empty_err)
        return self.success()

    @thrownException
    def generate_fee(self):
        param_schema = self.get_param_schema()
        logger.info("------[generate_fee]------")
        valid_res = self.check_form_valid(param_schema)
        logger.info(valid_res)
        if valid_res.return_code < 0:
            return valid_res
        pro_id = self.params.get("pro_id")
        if not pro_id:
            return self.failure(ERROR.pro_id_empty_err)
        pro_info = self.db.query(
            Pro_Info    
        ).filter(
            Pro_Info.id == pro_id
        ).first()
        if not pro_info:
            return self.failure(ERROR.pro_name_empty_err)
        env_id = pro_info.env_id
        env_resource_fee = self.db.query(
            Env_Resource_Fee
        ).filter(
            Env_Resource_Fee.env_id == env_id
        ).first()
        fee_dict = env_resource_fee.as_dict()
        computer_fee = fee_dict["computer"]
        cpu_fee = fee_dict["cpu"]
        mem_fee = fee_dict["memory"]
        disk_fee = fee_dict["disk"]
        disk_amount_fee = fee_dict.get("disk_amount", 0)
        disk_backup_fee = fee_dict["disk_backup"]
        disk_backup_amount_fee = fee_dict.get("disk_backup_amount", 0)
        out_ip_fee = fee_dict["out_ip"]
        snapshot_fee = fee_dict["snapshot"]
        loadbalance_fee = fee_dict["loadbalance"]
        internet_ip_fee_dict = fee_dict["internet_ip"]
        # bandwidth = fee_dict["bandwidth"]
        internet_ip_ssl_fee = fee_dict["internet_ip_ssl"] 

        logger.info(valid_res.data)
        params = valid_res.data
        computer = int(params.get("computer"))
        cpu = int(params.get("cpu"))
        mem = int(params.get("memory"))
        disk = int(params.get("disk"))
        disk_amount = int(params.get("disk_amount"))
        disk_backup = int(params.get("disk_backup"))
        disk_backup_amount = int(params.get("disk_backup_amount"))
        out_ip = int(params.get("out_ip"))
        snapshot = int(params.get("snapshot"))
        loadbalance = int(params.get("loadbalance"))
        internet_ip_id = int(params.get("internet_ip"))
        internet_ip_ssl = int(params.get("internet_ip_ssl"))
        bandwidth = int(params.get("bandwidth"))
        period = int(params.get("period"))

        _internet_ip_fee = 0 
        for i in internet_ip_fee_dict:
            if i["id"] == internet_ip_id:
                # _internet_ip_fee = i["fee"]
                bandwidth_fee_dict = i["fee"]
                _internet_ip_fee = bandwidth_fee_dict.get(str(bandwidth))
                break
            else:
                continue

        # TODO 完善计算费率
            # 云主机数量费用 \
            # CPU数量费用
            # 内存容量费用
            # 云磁盘数量费用
            # 合计云磁盘容量费用
            # 云磁盘备份数量费用
            # 云磁盘备份容量费用
            # 外部IP数量费用
            # 快照数量费用
            # 应用负载均衡数量费用
            # 互联网服务费用（单线、双线等）
            # 是否需要开通SSL费用
        unit_fee = computer_fee * computer \
            + cpu_fee * cpu \
            + mem_fee * mem \
            + disk_fee * disk \
            + disk_amount_fee * disk_amount \
            + disk_backup_amount_fee * disk_backup_amount \
            + disk_backup_fee * disk_backup \
            + out_ip * out_ip_fee \
            + snapshot * snapshot_fee \
            + loadbalance * loadbalance_fee \
            + float(_internet_ip_fee) \
            + internet_ip_ssl * internet_ip_ssl_fee

        if self.params.get('period') == 0:
            return self.failure(ERROR.res_period_empty_err)
        total_fee = unit_fee * period

        data = {
            "unit_fee": unit_fee,
            "total_fee": total_fee
        }
        return self.success(data=data)

    @thrownException
    def do_apply(self):
        logger.info("---------[do_apply]---------")
        param_schema = self.get_param_schema()
        form_valid_res = self.check_form_valid(param_schema)
        if form_valid_res.return_code < 0:
            return form_valid_res
        # form_empty_res = self.check_form_empty()
        # if form_empty_res.return_code < 0:
        #     return form_empty_res
        pro_id = self.params.get("pro_id")
        # user_id = self.params.get("user_id")
        user_id = self.handler.current_user.id
        logger.info(self.params)
        if not pro_id:
            return self.failure(ERROR.not_found_err)
        if not user_id:
            return self.failure(ERROR.user_empty_err)
        pro_info = self.db.query(
            Pro_Info
        ).filter(
            Pro_Info.id == pro_id
        ).first()
        generate_fee_res = self.generate_fee()
        if generate_fee_res.return_code == 0:
            fee_data = generate_fee_res.data
        else:
            fee_data = dict(unit_fee=0, total_fee=0)
            return generate_fee_res
        applies = pro_info.pro_resource_applies
        if len(applies) > 0:
            first_apply = applies[0]
            last_apply = applies[-1]
            # 状态为0、1时不能申请新配额
            logger.info("\t [last_apply status] %s" % last_apply.status)
            if last_apply.status >= 0 and last_apply.status < 2:
                return self.failure(ERROR.res_new_apply_err)
        else:
            first_apply = None
            last_apply = None
        params = form_valid_res.data
        apply = Pro_Resource_Apply()
        apply.pro_id = pro_id
        apply.computer = params.get('computer')
        apply.cpu = params.get('cpu')
        apply.memory = params.get('memory')
        apply.disk = params.get('disk')
        apply.disk_backup = params.get('disk_backup')
        apply.out_ip = params.get('out_ip')
        apply.snapshot = params.get('snapshot')
        apply.loadbalance = params.get('loadbalance')
        apply.internet_ip = params.get('internet_ip')
        apply.bandwidth = params.get('bandwidth')
        apply.internet_ip_ssl = params.get('internet_ip_ssl')
        apply.start_date = params.get('start_date')
        apply.period = params.get('period')
        apply.unit_fee = fee_data["unit_fee"]
        apply.total_fee = fee_data["total_fee"]
        apply.fee_desc = u"单月费用 %s（元/月）×有效期 %s（月）=总费用 %s（元）" % (fee_data['unit_fee'], params.get('period'), fee_data['total_fee'])
        apply.user_id = user_id
        apply.status = STATUS_RESOURCE.APPLIED
        apply.reason = u''
        if first_apply:
            apply.desc = u'资源调整'
        self.db.add(apply)
        self.db.flush()
        mail_html = self.render_to_string("admin/mail/pro_resource_apply_to_admin.html", resource_apply=apply, STATUS_RESOURCE=STATUS_RESOURCE)
        logger.info("<" + "=" * 60 + ">")
        logger.info(mail_html)
        # user_name = apply.user.email or apply.user.mobile
        mail_title = mail_title_format % {
            "user_name": apply.user.email or apply.user.mobile,
            "pro_name": apply.project.name,
            "res_desc": apply.desc,
            "action": u"申请的",
            "todo_action": u"资源，已提交，请审核",
        }
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        task_post_pro_res_apply_history.delay(status=apply.status, content=mail_title, pro_id=pro_id, res_apply_id=apply.id, user_id=user_id)
        # from scloud.views.admin.ws.pubsub import r
        # r.publish("test_realtime", "notice_checker")
        return self.success(data=apply)

    @thrownException
    def do_re_apply(self):
        logger.info("---------[do_re_apply]----------")
        param_schema = self.get_param_schema()
        form_valid_res = self.check_form_valid(param_schema)
        if form_valid_res.return_code < 0:
            return form_valid_res
        # form_empty_res = self.check_form_empty()
        # if form_empty_res.return_code < 0:
        #     return form_empty_res
        pro_id = self.params.get("pro_id")
        res_id = self.params.get("res_id")
        # user_id = self.params.get("user_id")
        user_id = self.handler.current_user.id
        if not pro_id:
            return self.failure(ERROR.not_found_err)
        if not res_id:
            return self.failure(ERROR.not_found_err)
        if not user_id:
            return self.failure(ERROR.user_empty_err)
        pro_info = self.db.query(
            Pro_Info
        ).filter(
            Pro_Info.id == pro_id
        ).first()
        if not pro_info:
            return self.failure(ERROR.not_found_err)
        resource = self.db.query(
            Pro_Resource_Apply
        ).filter(
            Pro_Resource_Apply.id == res_id
        ).first()
        if not resource:
            return self.failure(ERROR.not_found_err)
        generate_fee_res = self.generate_fee()
        if generate_fee_res.return_code == 0:
            fee_data = generate_fee_res.data
        else:
            fee_data = dict(unit_fee=0, total_fee=0)
            return generate_fee_res
        params = form_valid_res.data
        logger.info("\t form_valid_res data: %s" % params)
        resource.computer = params.get('computer')
        resource.cpu = params.get('cpu')
        resource.memory = params.get('memory')
        resource.disk = params.get('disk')
        resource.disk_amount = params.get('disk_amount')
        resource.disk_backup = params.get('disk_backup')
        resource.disk_backup_amount = params.get('disk_backup_amount')
        resource.out_ip = params.get('out_ip')
        resource.snapshot = params.get('snapshot')
        resource.loadbalance = params.get('loadbalance')
        resource.internet_ip = params.get('internet_ip')
        resource.bandwidth = params.get('bandwidth')
        resource.internet_ip_ssl = params.get('internet_ip_ssl')
        resource.start_date = params.get('start_date')
        resource.period = params.get('period')
        resource.unit_fee = fee_data['unit_fee']
        resource.total_fee = fee_data['total_fee']
        resource.fee_desc = u"单月费用 %s（元/月）×有效期 %s（月）=总费用 %s（元）" % (fee_data['unit_fee'], params.get('period'), fee_data['total_fee'])
        resource.status = STATUS_RESOURCE.APPLIED
        resource.reason = u''
        self.db.add(resource)
        self.db.flush()
        mail_html = self.render_to_string("admin/mail/pro_resource_apply_to_admin.html", resource_apply=resource, STATUS_RESOURCE=STATUS_RESOURCE)
        mail_title = mail_title_format % {
            "user_name": resource.user.email or resource.user.mobile,
            "pro_name": resource.project.name,
            "res_desc": resource.desc,
            "action": u"申请的",
            "todo_action": u"资源，已重新提交，请审核",
        }
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        task_post_pro_res_apply_history.delay(status=resource.status, content=mail_title, pro_id=resource.project.id, res_apply_id=resource.id, user_id=user_id)
        # from scloud.views.admin.ws.pubsub import r
        # r.publish("test_realtime", "notice_checker")
        return self.success(data=resource)

    @thrownException
    def do_revoke(self):
        res_id = self.params.get("res_id", 0)
        # user_id = self.params.get("user_id", 0)
        user_id = self.handler.current_user.id
        resource = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
        if not resource:
            return self.failure(ERROR.not_found_err)
        # 状态不为0（即：不是提交状态），不允许撤销
        if resource.status != 0:
            return self.failure(ERROR.res_revoke_err)
        resource.status = STATUS_RESOURCE.REVOKED
        self.db.add(resource)
        self.db.flush()
        mail_html = self.render_to_string("admin/mail/pro_resource_apply_to_admin.html", resource_apply=resource, STATUS_RESOURCE=STATUS_RESOURCE)
        mail_title = mail_title_format % {
            "user_name": resource.user.email or resource.user.mobile,
            "pro_name": resource.project.name,
            "res_desc": resource.desc,
            "action": u"申请的",
            "todo_action": u"资源，已撤销",
        }
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        task_post_pro_res_apply_history.delay(status=resource.status, content=mail_title, pro_id=resource.project.id, res_apply_id=resource.id, user_id=user_id)
        # from scloud.views.admin.ws.pubsub import r
        # r.publish("test_realtime", "notice_checker")
        return self.success(data=resource)

    @thrownException
    def do_delete(self):
        res_id = self.params.get("res_id", 0)
        logger.info("\t res_id : %s" % res_id)
        # user_id = self.params.get("user_id", 0)
        user_id = self.handler.current_user.id
        resource = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
        if not resource:
            return self.failure(ERROR.not_found_err)
        # 状态只有-1、-2（即：已撤销、申请被拒绝）可以删除
        if resource.status > STATUS_RESOURCE.REVOKED:
            return self.failure(ERROR.res_delete_err)
        # resource.status = STATUS_RESOURCE.DELETED
        # self.db.add(resource)
        mail_content = mail_format % {
            "pro_name": resource.project.name,
            "pro_id": resource.project.id,
            "user_name": resource.user.email or resource.user.mobile,
            "resource_status": "已删除",
        }
        resource.is_enable = False
        # resource.status = STATUS_RESOURCE.DELETED
        self.db.add(resource)
        # self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).delete()
        # resource.delete()
        self.db.flush()
        logger.info("\t resource is deleted")
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_content, mail_content)
        task_post_pro_res_apply_history.delay(status=resource.status, content=mail_content, pro_id=resource.project.id, res_apply_id=resource.id, user_id=user_id)
        # from scloud.views.admin.ws.pubsub import r
        # r.publish("test_realtime", "notice_checker")
        return self.success(data=resource)

    @thrownException
    def do_pay(self):
        logger.info("\t [ DO PAY ]")
        res_id = self.params.get("res_id", 0)
        user_id = self.params.get("user_id", 0)
        user_id = self.handler.current_user.id
        resource_query = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id)
        logger.info("\t [QUERY] : %s" % resource_query)
        resource = resource_query.first()
        if not resource:
            # return self.failure(ERROR.not_found_err)
            return NotFoundError()
        # 状态不为0（即：不是提交状态），不允许撤销
        logger.info("\t [resource.status]: %s" % resource.status)
        logger.info("\t [STATUS_RESOURCE.CHECKED]: %s" % STATUS_RESOURCE.CHECKED)
        logger.info("\t change to [STATUS_RESOURCE.PAYED]: %s" % STATUS_RESOURCE.PAYED)
        if resource.status != STATUS_RESOURCE.CHECKED:
            return self.failure(ERROR.res_pay_err)
        resource.status = STATUS_RESOURCE.PAYED
        self.db.add(resource)
        self.db.flush()
        mail_html = self.render_to_string("admin/mail/pro_resource_apply_to_admin.html", resource_apply=resource, STATUS_RESOURCE=STATUS_RESOURCE)
        mail_title = mail_title_format % {
            "user_name": resource.user.email or resource.user.mobile,
            "pro_name": resource.project.name,
            "res_desc": resource.desc,
            "action": u"申请的",
            "todo_action": u"资源，已完成支付，请确认收款",
        }
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        task_post_pro_res_apply_history.delay(status=resource.status, content=mail_title, pro_id=resource.project.id, res_apply_id=resource.id, user_id=user_id)
        # from scloud.views.admin.ws.pubsub import r
        # r.publish("test_realtime", "notice_checker")
        return self.success(data=resource)

    @thrownException
    def set_start(self):
        res_id = self.params.get("res_id", 0)
        start_date = self.params.get("start_date", None)
        resource = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
        if not resource:
            return self.failure(ERROR.not_found_err)
        # 状态只有-1、-2（即：已撤销、申请被拒绝）可以删除
        if resource.status <= -1:
            return self.failure(ERROR.res_delete_err)
        resource.start_date = start_date
        # self.db.add(resource)
        self.db.flush()
        mail_html = self.render_to_string("admin/mail/pro_resource_apply_to_admin.html", resource_apply=resource, STATUS_RESOURCE=STATUS_RESOURCE)
        mail_title = mail_title_format % {
            "user_name": resource.user.email or resource.user.mobile,
            "pro_name": resource.project.name,
            "res_desc": resource.desc,
            "action": u"申请的",
            "todo_action": u"资源，已设置启用时间",
        }
        sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        task_post_pro_res_apply_history.delay(status=resource.status, content=mail_title, pro_id=resource.project.id, res_apply_id=resource.id, user_id=self.handler.current_user.id)
        return self.success(data=resource)


class ProResourceCheckService(BaseService):
    @thrownException
    def get_resource(self):
        res_id = self.params.get("res_id", 0)
        resource = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
        return self.success(data=resource)

    @thrownException
    def get_resources_by_status(self):
        logger.info("\t ==========[ get_resources_by_status ]==========")
        conditions = and_()
        res_status = self.params.get("res_status")
        if res_status:
            conditions.append(Pro_Resource_Apply.status == res_status)
        env_id = self.params.get("env_id", 0)
        if env_id:
            conditions.append(Pro_Info.env_id == env_id)
        logger.info("\t [res_status]: %s" % res_status)
        resource_list = self.db.query(
            Pro_Resource_Apply
        ).outerjoin(
            Pro_Info, Pro_Info.id == Pro_Resource_Apply.pro_id
        ).filter(
            conditions
        ).order_by(
            Pro_Resource_Apply.create_time.desc()
        ).all()

        # 按状态查询申请数量
        status_counts = self.db.query(
            Pro_Resource_Apply.status, func.count(Pro_Resource_Apply.id)
        ).group_by(
            Pro_Resource_Apply.status
        ).all()
        status_counts = dict(status_counts)
        logger.info("status_counts: %s" % status_counts)

        # 按环境查询申请数量
        env_counts = self.db.query(
            Pro_Info.env_id, func.count(Pro_Resource_Apply.id)
        ).outerjoin(
            Pro_Resource_Apply, Pro_Resource_Apply.pro_id == Pro_Info.id
        ).outerjoin(
            Env_Info, Env_Info.id == Pro_Info.env_id
        ).group_by(
            Env_Info.id
        ).all()
        env_counts = dict(env_counts)
        logger.info("env_counts: %s" % env_counts)

        data = ObjectDict()
        data.resource_list = resource_list
        data.status_counts = status_counts
        data.env_counts = env_counts
        return self.success(data=data)

    @thrownException
    def do_resource_action(self):
        """
            针对管理员修改资源申请状态
        """
        res_ids = self.params.get("res_ids", "")
        checker_id = self.params.get("checker_id", 0)
        action = self.params.get("action", "")
        reason = self.params.get("reason", "")
        logger.info("\t action: %s, STATUS_RESOURCE.refused.value_en: %s" % (action, STATUS_RESOURCE.refused.value_en))
        logger.info("\t reason: %s" % reason)
        if action == STATUS_RESOURCE.refused.value_en:
            if not reason:
                return self.failure(ERROR.res_reason_empty_err)
        actions = [STATUS_RESOURCE.get(i).value_en for i in STATUS_RESOURCE.keys() if isinstance(i, int)]
        logger.info("\t [actions] : %s" % actions)
        if action not in actions:
            return self.failure(ERROR.res_do_resource_action_err)
        res_id_list = [int(i) for i in res_ids.split(",") if i.isdigit()]
        email_list = []
        tip_messages = []
        logger.info("<"+"start for"+">")
        logger.info("< %s >" % res_id_list)
        def _get_message(msg=u"", err=None, level="success"):
            if msg:
                return u"%s" % msg, "%s" % level
            elif err:
                return u"(%s)%s" % (err.errcode, err.errvalue), "%s" % level
            return u""
        for res_id in res_id_list:
            resource = self.db.query(Pro_Resource_Apply).filter(Pro_Resource_Apply.id == res_id).first()
            if not resource:
                tip_messages.append(_get_message(err=ERROR.not_found_err, level="warning"))
                continue
            email = resource.user.email

            previous_status = STATUS_RESOURCE.get(action.upper()) - 1
            if action == STATUS_RESOURCE.refused.value_en:
                previous_status = STATUS_RESOURCE.APPLIED
            if action == STATUS_RESOURCE.applied.value_en:
                previous_status = STATUS_RESOURCE.CHECKED
            logger.info("<" + "#" * 60 + ">")
            logger.info(resource.status)
            if resource.status != previous_status:
                if action == STATUS_RESOURCE.checked.value_en:
                    tip_messages.append(_get_message(err=ERROR.res_check_err, level="warning"))
                elif action == STATUS_RESOURCE.refused.value_en:
                    tip_messages.append(_get_message(err=ERROR.res_refuse_err, level="warning"))
                elif action == STATUS_RESOURCE.confirmpayed.value_en:
                    tip_messages.append(_get_message(err=ERROR.res_confirmpay_err, level="warning"))
                elif action == STATUS_RESOURCE.started.value_en:
                    tip_messages.append(_get_message(err=ERROR.res_start_err, level="warning"))
                elif action == STATUS_RESOURCE.closed.value_en:
                    tip_messages.append(_get_message(err=ERROR.res_close_err, level="warning"))
                else:
                    tip_messages.append(_get_message(err=ERROR.res_do_resource_action_err, level="warning"))
                continue
            resource.status = STATUS_RESOURCE.get(action.upper())
            # if action == STATUS_RESOURCE.refused.value_en:
            #     reason = self.params.get("reason", "")
            resource.reason = reason
            resource.checker_id = checker_id
            # logger.info(resource.status)
            # logger.info("<"+"#"*60+">")
            self.db.add(resource)
            self.db.flush()
            mail_html = self.render_to_string("admin/mail/pro_resource_apply.html", resource_apply=resource, STATUS_RESOURCE=STATUS_RESOURCE)
            mail_title = mail_title_format % {
                "user_name": resource.checker.email or resource.checker.mobile,
                "pro_name": resource.project.name,
                "res_desc": resource.desc,
                "action": u"审核的",
                "todo_action": u"资源，%s，%s" % (STATUS_RESOURCE.get(resource.status).value, STATUS_RESOURCE.get(resource.status).todo_value),
            }
            email_list.append((email, mail_html))
            tip_messages.append(_get_message(msg=mail_title))
            task_post_pro_res_apply_history.delay(status=resource.status, content=mail_title, pro_id=resource.project.id, res_apply_id=resource.id, user_id=resource.user_id, checker_id=checker_id)
            publish_notice_user.delay(resource.user_id)

        email_dict = {}
        for email, mail_content in email_list:
            if email_dict.get(email):
                email_dict[email].append(mail_content)
            else:
                email_dict[email] = [mail_content]
        logger.info("\t [email_dict]%s" % email_dict)

        for email, mail_content_list in email_dict.items():
            sendMail.delay("scloud@infohold.com.cn", [email], u"资源%s通知" % STATUS_RESOURCE.get(action).act_value, "\n\n".join(mail_content_list))
        # from scloud.views.admin.ws.pubsub import r
        # r.publish("test_realtime", "notice_user")
        return self.success(data=tip_messages)
