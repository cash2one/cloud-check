#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.models.base import BaseModel, BaseModelMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode, Integer, Float, String


class Env_Info(BaseModel, BaseModelMixin):
    u"""项目环境"""
    __tablename__ = "env_info"
    name = Column(Unicode, unique=True, default=u'')
    desc = Column(Unicode, default=u'')


class Env_Internet_Ip_Types(BaseModel, BaseModelMixin):
    u"""互联网IP分类"""
    __tablename__ = "env_internet_ip_types"
    env_id = Column(Integer, ForeignKey('env_info.id'), default=0)
    name = Column(Unicode, unique=True, default=u'')
    desc = Column(Unicode, default=u'')
    env = relationship("Env_Info", backref="env_internet_ip_types")


class Env_Resource_Fee(BaseModel, BaseModelMixin):
    u"""项目资源申请"""
    __tablename__ = "env_resource_fee"
    env_id = Column(Integer, ForeignKey('env_info.id'), default=0)
    computer = Column(Float, default=0.00)
    cpu = Column(Float, default=0.00)
    memory = Column(Float, default=0.00)
    disk = Column(Float, default=0.00)
    disk_backup = Column(Float, default=0.00)
    out_ip = Column(Float, default=0.00)
    snapshot = Column(Float, default=0.00)
    loadbalance = Column(Float, default=0.00)
    internet_ip = Column(String, default="")
    internet_ip_ssl = Column(Float, default=0.00)
    env = relationship("Env_Info", backref="env_resource_fees")


class Env_Resource_Value(BaseModel, BaseModelMixin):
    u"""项目资源申请"""
    __tablename__ = "env_resource_value"
    env_id = Column(Integer, ForeignKey('env_info.id'), default=0)
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
    env = relationship("Env_Info", backref="env_resource_values")
