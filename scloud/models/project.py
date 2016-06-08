#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from datetime import datetime, timedelta
from scloud.config import logger
from scloud.models.base import BaseModel, BaseModelMixin
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Info, Env_Internet_Ip_Types
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
    BRIEF = "PRO"

    name = Column(Unicode, default=u'')
    owner = Column(Unicode, default=u'')
    owner_email = Column(Unicode, default=u'')
    owner_mobile = Column(Unicode, default=u'')
    env_id = Column(Integer, ForeignKey("env_info.id"), default=0)
    desc = Column(Unicode, default=u'')
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')
    is_enable = Column(Integer, default=1)

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_infos")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_infos")
    env = relationship("Env_Info", backref="pro_infos")


class Pro_Resource_Apply(BaseModel, BaseModelMixin, Pro_Resource_Apply_Mixin):
    u"""项目资源申请"""
    __tablename__ = "pro_resource_apply"
    BRIEF = "APY"

    pro_id = Column(Integer, ForeignKey("pro_info.id"), default=0, info=u"资源申请编号")
    computer = Column(Integer, default=0, info={"name": u"云主机数量", "unit": u"个", "tip": u"云主机的最大数量"})
    cpu = Column(Integer, default=0, info={"name": u"CPU数量", "unit": u"个", "tip": u"VCPU的最大个数"})
    memory = Column(Integer, default=0, info={"name": u"内存容量", "unit": u"GB", "tip": u"内存的最大合计容量"})
    disk = Column(Integer, default=0, info={"name": u"云磁盘数量", "unit": u"个", "tip": u"除云主机模板自带的磁盘外，额外挂载的磁盘数量"})
    disk_amount = Column(Integer, default=0, info={"name": u"合计", "unit": u"GB", "tip": u"额外挂载的总磁盘容量"})
    disk_backup = Column(Integer, default=0, info={"name": u"云磁盘备份数量", "unit": u"个", "tip": u""})
    disk_backup_amount = Column(Integer, default=0, info={"name": u"文件备份空间", "unit": u"GB", "tip": u"需要备份的文件空间总容量"})
    out_ip = Column(Integer, default=0, info={"name": u"外部IP数量", "unit": u"个", "tip": u"云主机的外部IP，用一与其他项目交互或与互联网交互，没需求可不用"})
    snapshot = Column(Integer, default=0, info={"name": u"快照数量", "unit": u"个", "tip": u"云主机快照数量"})
    loadbalance = Column(Integer, default=0, info={"name": u"应用负载均衡", "unit": u"个VSERVER", "tip": u"负载均衡vserver数量"})
    # internet_ip = Column(Integer, default=0, info={"name": u"互联网IP"})
    internet_ip = Column(Integer, ForeignKey("env_internet_ip_types.id"), info={"name": u"是否发布互联网服务", "tip": u""})
    internet_ip_ssl = Column(Integer, default=0, info={"name": u"是否需要SSL卸载", "tip": u""})
    bandwidth = Column(Integer, default=0, info={"name": u"互联网带宽", "tip": u"根据需要选择适合的带宽容量"})
    desc = Column(Unicode, default=u'资源申请', info={"name": u"资源申请描述", "tip": u""})
    start_date = Column(DateTime, default=func.now(), info={"name": u"启用时间", "tip": u"运行时间一般为每月1号，所有的费用产生都是从1号开始计费"})
    period = Column(Integer, default=0, info={"name": u"运行有效期", "unit": u"个月", "tip": u""})
    due_date = Column(DateTime, default=default_due_date, info={"name": u"到期时间", "tip": u""})
    unit_fee = Column(Float, default=0.00, info={"name": u"单月费用", "unit": u"元/月", "tip": u""})
    total_fee = Column(Float, default=0.00, info={"name": u"总费用", "unit": u"元", "tip": u""})
    fee_desc = Column(Unicode, default=u'', info={"name": u"产生费用描述", "tip": u""})
    status = Column(Integer, default=0, info={"name": u"资源申请状态", "tip": u""})
    reason = Column(Unicode, default=u'', info={"name": u"资源申请拒绝原因", "tip": u""})
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')
    is_enable = Column(Integer, default=1)

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_resource_applies")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_resource_applies")
    project = relationship("Pro_Info", backref=backref("pro_resource_applies", order_by="Pro_Resource_Apply.id"))
    internet_ip_obj = relationship("Env_Internet_Ip_Types", backref=backref("pro_resource_applies", order_by="Pro_Resource_Apply.update_time"))


class Pro_User(BaseModel, BaseModelMixin):
    u"""权限用户"""
    __tablename__ = "pro_user"
    BRIEF = "USR"

    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    status = Column(Integer, default=0, info=u"申请状态")
    reason = Column(Unicode, default=u'', info={"name": u"权限用户拒绝原因"})
    email = Column(Unicode, default=u'', info=u"邮箱")
    username = Column(Unicode, default=u'', info=u"用户名") 
    is_enable = Column(Integer, default=1, info=u"是否可用")
    user_type = Column(Integer, default=0, info=u"用户类型")
    desc = Column(Unicode, default=u'', info=u"权限描述") 
    use_vpn = Column(Integer, default=0, info=u"是否需要开通VPN远程访问")
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')

    user = relationship("PT_User", foreign_keys=[user_id], backref="pro_users")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_pro_users")
    project = relationship("Pro_Info", backref=backref("pro_users", order_by="Pro_User.update_time"))

    @property
    def brief(self):
        return "USR"


class Pro_Publish(BaseModel, BaseModelMixin):
    u"""互联网发布"""
    __tablename__ = "pro_publish"
    BRIEF = "PUB"

    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    status = Column(Integer, default=0, info=u"申请状态")
    reason = Column(Unicode, default=u'', info={"name": u"互联网发布拒绝原因"})
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
    BRIEF = "BAL"
    json_columns = [
        "members"
    ]
    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    res_apply_id = Column("res_apply_id", Integer, ForeignKey("pro_resource_apply.id"), default=0, info=u"所属资源申请")
    status = Column(Integer, default=0, info=u"申请状态")
    reason = Column(Unicode, default=u'', info={"name": u"负载均衡拒绝原因"})
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
    loadbalance = relationship("Pro_Balance", backref=backref("pro_loadbalance_members", order_by="Pro_Balance_Members.update_time"))


class Pro_Backup(BaseModel, BaseModelMixin):
    u"""定期备份"""
    __tablename__ = "pro_backup"
    BRIEF = "BAK"
    json_columns = [
        "plot"
    ]
    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    res_apply_id = Column("res_apply_id", Integer, ForeignKey("pro_resource_apply.id"), default=0, info=u"所属资源申请")
    status = Column(Integer, default=0, info=u"申请状态")
    reason = Column(Unicode, default=u'', info={"name": u"定期备份拒绝原因"})
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
    BRIEF = "EVT"

    pro_id = Column("pro_id", Integer, ForeignKey("pro_info.id"), default=0, info=u"所属项目")
    res_apply_id = Column("res_apply_id", Integer, ForeignKey("pro_resource_apply.id"), default=0, info=u"所属资源申请")
    status = Column(Integer, default=0, info=u"申请状态")
    reason = Column(Unicode, default=u'', info={"name": u"事件工单拒绝原因"})
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
