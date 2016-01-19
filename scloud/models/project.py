#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.models.base import BaseModel, BaseModelMixin
from sqlalchemy import Column, func
from sqlalchemy.types import Unicode, Integer, Float, DateTime


class Pro_Info(BaseModel, BaseModelMixin):
    u"""项目信息表"""
    __tablename__ = "pro_info"
    name = Column(Unicode, default=u'')
    owner_id = Column(Integer, default=0)
    env_id = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')


class Pro_Resource_Apply(BaseModel, BaseModelMixin):
    __tablename__ = "pro_resource_apply"
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
    desc = Column(Unicode, default=u'创建项目')
    start_time = Column(DateTime, default=func.now())
    period = Column(Integer, default=0)
    due_time = Column(DateTime, default=func.now())
    fee_current_mouth = Column(Float, default=0.00)
    fee_total = Column(Float, default=0.00)
    fee_desc = Column(Unicode, default=u'')


class Pro_Environment(BaseModel, BaseModelMixin):
    __tablename__ = "pro_environment"
    name = Column(Unicode, unique=True, default=u'')
    desc = Column(Unicode, default=u'')


class Pro_Internet_Ip_Types(BaseModel, BaseModelMixin):
    __tablename__ = "pro_internet_ip_types"
    name = Column(Unicode, unique=True, default=u'')
    desc = Column(Unicode, default=u'')
