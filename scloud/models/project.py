#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from datetime import datetime, timedelta
from scloud.config import logger
from scloud.models.base import BaseModel, BaseModelMixin
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Info
from scloud.models.project_mixin import Pro_Info_Mixin, Pro_Resource_Apply_Mixin
from sqlalchemy import Column, func, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Unicode, Integer, Float, DateTime


def get_due_date(current, months):
    logger.info("\t [get_due_date]")
    if not current:
        logger.info("\t [current]: %s" % current)
        return False
    if not months:
        logger.info("\t [current]: %s" % months)
        return False
    if not isinstance(months, int) and not isinstance(months, long):
        logger.info("\t [current instance]: %s" % type(months))
        return False
    if not isinstance(current, datetime):
        current = datetime.strptime(current, "%Y-%m-%d %H:%M:%S")
    # current = context.current_parameters['start_date']
    # months = context.current_parameters['period']
    dateformat = "%s-%02d-%s" % (current.year + (current.month + months) / 12, (current.month + months) % 12, 1)
    due_date = datetime.strptime(dateformat, "%Y-%m-%d")
    due_date = due_date + timedelta(seconds=-1)
    return due_date

def default_due_date(context):
    current = context.current_parameters['start_date']
    months = context.current_parameters['period']
    result = get_due_date(current, months)
    if result:
        return result
    else:
        return '0000-00-00'
    # dateformat = "%s-%02d-%s" % (current.year + (current.month + months) / 12, (current.month + months) % 12, 1)
    # due_date = datetime.strptime(dateformat, "%Y-%m-%d")
    # due_date = due_date + timedelta(days=-1)
    # return due_date


class Pro_Info(BaseModel, BaseModelMixin, Pro_Info_Mixin):
    u"""项目信息"""
    __tablename__ = "pro_info"
    name = Column(Unicode, default=u'')
    owner = Column(Unicode, default=u'')
    owner_email = Column(Unicode, default=u'')
    owner_mobile = Column(Unicode, default=u'')
    env_id = Column(Integer, ForeignKey("env_info.id"), default=0)
    desc = Column(Unicode, default=u'')
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_infos")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_infos")
    env = relationship("Env_Info", backref="pro_infos")


class Pro_Resource_Apply(BaseModel, BaseModelMixin, Pro_Resource_Apply_Mixin):
    u"""项目资源申请"""
    __tablename__ = "pro_resource_apply"
    pro_id = Column(Integer, ForeignKey("pro_info.id"), default=0, info=u"资源申请编号")
    computer = Column(Integer, default=0, info={"name": u"云主机数量", "unit": u"个"})
    cpu = Column(Integer, default=0, info={"name": u"CPU数量", "unit": u"个"})
    memory = Column(Integer, default=0, info={"name": u"内存容量", "unit": u"GB"})
    disk = Column(Integer, default=0, info={"name": u"云磁盘数量", "unit": u"个"})
    disk_backup = Column(Integer, default=0, info={"name": u"云磁盘备份数量", "unit": u"个"})
    out_ip = Column(Integer, default=0, info={"name": u"外部IP", "unit": u"个"})
    snapshot = Column(Integer, default=0, info={"name": u"快照", "unit": u"个"})
    loadbalance = Column(Integer, default=0, info={"name": u"负载均衡", "unit": u"个"})
    internet_ip = Column(Integer, default=0, info={"name": u"互联网IP"})
    internet_ip_ssl = Column(Integer, default=0, info={"name": u"是否需要SSL卸载"})
    desc = Column(Unicode, default=u'资源申请', info={"name": u"资源申请描述"})
    start_date = Column(DateTime, default=func.now(), info={"name": u"启用时间"})
    period = Column(Integer, default=0, info={"name": u"运行有效期", "unit": u"月"})
    due_date = Column(DateTime, default=default_due_date, info={"name": u"到期时间"})
    unit_fee = Column(Float, default=0.00, info={"name": u"单月费用", "unit": u"元"})
    total_fee = Column(Float, default=0.00, info={"name": u"总费用", "unit": u"元"})
    fee_desc = Column(Unicode, default=u'', info={"name": u"产生费用描述"})
    status = Column(Integer, default=0, info={"name": u"资源申请状态"})
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_resource_applies")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_resource_applies")
    project = relationship("Pro_Info", backref=backref("pro_resource_applies", order_by="Pro_Resource_Apply.update_time"))


class Pro_User(BaseModel, BaseModelMixin):
    u"""权限用户"""
    __tablename__ = "pro_user"
    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    status = Column(Integer, default=0, info=u"申请状态")
    email = Column(Unicode, default=u'', info=u"邮箱")
    username = Column(Unicode, default=u'', info=u"用户名") 
    is_enable = Column(Integer, default=1, info=u"是否可用")
    use_vpn = Column(Integer, default=0, info=u"是否需要开通VPN远程访问")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_users")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_users")
    project = relationship("Pro_Info", backref=backref("pro_users", order_by="Pro_User.update_time"))


class Pro_Publish(BaseModel, BaseModelMixin):
    u"""互联网发布"""
    __tablename__ = "pro_publish"
    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    status = Column(Integer, default=0, info=u"申请状态")
    domain = Column("domain", Unicode, default=u'', info=u"域名")
    domain_port = Column("domain_port", Integer, default=80, info=u"互联网端口")
    network_address = Column("network_address", Unicode, default=u'', info=u"内网地址")
    network_port = Column("network_port", Integer, default=80, info=u"内网端口")
    use_ssl = Column("use_ssl", Integer, default=0, info=u"是否需要SSL卸载")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_publishs")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_publishs")
    project = relationship("Pro_Info", backref=backref("pro_publish_list", order_by="Pro_Publish.update_time"))


class Pro_Balance(BaseModel, BaseModelMixin):
    u"""负载均衡"""
    __tablename__ = "pro_balance"
    json_columns = [
        "members"
    ]
    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    res_apply_id = Column("res_apply_id", Integer, ForeignKey("pro_resource_apply.id"), default=0, info=u"所属资源申请")
    status = Column(Integer, default=0, info=u"申请状态")
    members = Column("members", Unicode, default=u'', info=u"成员")
    plot = Column("plot", Integer, default=0, info=u"策略")
    health = Column("health", Integer, default=0, info=u"策略")
    url = Column("url", Unicode, default=u'', info=u"URL（仅限HTTP方式）")
    keyword = Column("keyword", Unicode, default=u'', info=u"关键字（仅限HTTP方式）")
    desc = Column("desc", Unicode, default=u'', info=u"特殊说明")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_balances")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_balances")
    res_apply = relationship("Pro_Resource_Apply", backref=backref("loadbalance_plot", uselist=False))
    project = relationship("Pro_Info", backref=backref("pro_balance_list", order_by="Pro_Balance.update_time"))


class Pro_Balance_Members(BaseModel, BaseModelMixin):
    u"""负载均衡成员"""
    __tablename__ = "pro_balance_members"
    pro_balance_id = Column(Integer, ForeignKey("pro_balance.id"), default=0, info=u"负载均衡")
    ip = Column("ip", Unicode, default=u'', info=u"IP地址")
    port = Column("port", Unicode, default=u'', info=u"端口")
    loadbalance = relationship("Pro_Balance", backref=backref("pro_loadbalance_members", order_by="Pro_Backup.update_time"))


class Pro_Backup(BaseModel, BaseModelMixin):
    u"""定期备份"""
    __tablename__ = "pro_backup"
    json_columns = [
        "plot"
    ]
    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    res_apply_id = Column("res_apply_id", Integer, ForeignKey("pro_resource_apply.id"), default=0, info=u"所属资源申请")
    status = Column(Integer, default=0, info=u"申请状态")
    plot = Column("plot", Unicode, default=u'', info=u"策略(json)")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_backups")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_backups")
    res_apply = relationship("Pro_Resource_Apply", backref=backref("backups_plot", uselist=False))
    project = relationship("Pro_Info", backref=backref("pro_backup_list", order_by="Pro_Backup.update_time"))


class Pro_Event(BaseModel, BaseModelMixin):
    u"""事件工单"""
    __tablename__ = "pro_event"

    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    res_apply_id = Column("res_apply_id", Integer, ForeignKey("pro_resource_apply.id"), default=0, info=u"所属资源申请")
    status = Column(Integer, default=0, info=u"申请状态")
    priority = Column(Integer, default=0, info=u"优先级别")
    title = Column("title", Unicode, default=u'', info=u"事件标题")
    content = Column(Unicode, default=u'', info=u"事件内容")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_events")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_events")
    res_apply = relationship("Pro_Resource_Apply", backref=backref("pro_events", uselist=False))
    project = relationship("Pro_Info", backref=backref("pro_events", order_by="Pro_Event.update_time"))


class Pro_Event_Detail(BaseModel, BaseModelMixin):
    u"""事件工单详情"""
    __tablename__ = "pro_event_detail"

    event_id = Column(Integer, ForeignKey("pro_event.id"), default=0, info=u"所属项目")
    content = Column(Unicode, default=u'', info=u"事件内容")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_event_details")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_event_details")
    event = relationship("Pro_Event", backref=backref("pro_event_details", order_by="Pro_Event_Detail.update_time"))
