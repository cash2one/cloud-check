#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.models.base import BaseModel, BaseModelMixin
from scloud.models.environment import Env_Info
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode, Integer, Float, DateTime


class Pro_Info(BaseModel, BaseModelMixin):
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
    desc = Column(Unicode, default=u'创建资源')
    start_time = Column(DateTime, default=func.now())
    period = Column(Integer, default=0)
    due_time = Column(DateTime, default=func.now())
    unit_fee = Column(Float, default=0.00)
    total_fee = Column(Float, default=0.00)
    fee_desc = Column(Unicode, default=u'')
    status = Column(Integer, default=0)
    project = relationship("Pro_Info", backref="pro_resource_applies")
