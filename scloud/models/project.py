#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from datetime import datetime, timedelta
from scloud.models.base import BaseModel, BaseModelMixin
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Info
from scloud.models.project_mixin import Pro_Info_Mixin
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Unicode, Integer, Float, DateTime


def get_due_date(context):
    current = context.current_parameters['start_date']
    months = context.current_parameters['period']
    dateformat = "%s-%02d-%s" % (current.year + (current.month + months) / 12, (current.month + months) % 12, 1)
    due_date = datetime.strptime(dateformat, "%Y-%m-%d")
    due_date = due_date + timedelta(days=-1)
    return due_date


class Pro_Info(BaseModel, BaseModelMixin, Pro_Info_Mixin):
    u"""项目信息"""
    __tablename__ = "pro_info"
    name = Column(Unicode, default=u'')
    owner = Column(Unicode, default=u'')
    owner_email = Column(Unicode, default=u'')
    owner_mobile = Column(Unicode, default=u'')
    env_id = Column(Integer, ForeignKey("env_info.id"), default=0)
    desc = Column(Unicode, default=u'')
    env = relationship("Env_Info", backref="pro_infos")


class Pro_Resource_Apply(BaseModel, BaseModelMixin):
    u"""项目资源申请"""
    __tablename__ = "pro_resource_apply"
    pro_id = Column(Integer, ForeignKey("pro_info.id"), default=0)
    computer = Column(Integer, default=0)
    cpu = Column(Integer, default=0)
    memory = Column(Integer, default=0)
    disk = Column(Integer, default=0)
    disk_backup = Column(Integer, default=0)
    out_ip = Column(Integer, default=0)
    snapshot = Column(Integer, default=0)
    loadbalance = Column(Integer, default=0)
    internet_ip = Column(Integer, default=0)
    internet_ip_ssl = Column(Integer, default=0)
    desc = Column(Unicode, default=u'资源申请')
    start_date = Column(DateTime, default=func.now())
    period = Column(Integer, default=0)
    due_date = Column(DateTime, default=get_due_date)
    unit_fee = Column(Float, default=0.00)
    total_fee = Column(Float, default=0.00)
    fee_desc = Column(Unicode, default=u'')
    status = Column(Integer, default=0)
    # user_id = Column(Integer, default=0)
    user_id = Column("user_id", Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, default=0)
    check_time = Column(DateTime, default='0000-00-00 00:00:00')
    user = relationship("PT_User", backref="pro_resource_applies")
    project = relationship("Pro_Info", backref=backref("pro_resource_applies", order_by="Pro_Resource_Apply.update_time"))
