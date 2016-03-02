#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from datetime import datetime, timedelta
from scloud.config import logger
from scloud.models.base import BaseModel, BaseModelMixin
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Info
from scloud.models.project_mixin import Pro_Info_Mixin
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


class Pro_Resource_Apply(BaseModel, BaseModelMixin):
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
