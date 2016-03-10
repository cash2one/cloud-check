#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.models.base import BaseModel, BaseModelMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Unicode, Integer, Float, String


class Env_Info(BaseModel, BaseModelMixin):
    u"""项目环境"""
    __tablename__ = "env_info"
    name = Column(Unicode(256), unique=True, default=u'')
    desc = Column(Unicode(512), default=u'')


class Env_Internet_Ip_Types(BaseModel, BaseModelMixin):
    u"""互联网IP分类"""
    __tablename__ = "env_internet_ip_types"
    env_id = Column(Integer, ForeignKey('env_info.id', ondelete="CASCADE"), default=0)
    name = Column(Unicode(256), unique=True, default=u'', info={"name": u"互联网IP分类名称", "placeholder": u"如单线、双线等"})
    desc = Column(Unicode(512), default=u'', info={"name": "互联网IP分类描述"})
    fee = Column(Float(11,2), default=0.00, info={"name": u"相关费用（元）"})
    # env = relationship("Env_Info", backref=backref("env_internet_ip_types"))
    env = relationship("Env_Info", backref=backref("env_internet_ip_types",
                           cascade="all,delete,delete-orphan",
                           passive_deletes=True
                       ))


class Env_Resource_Fee(BaseModel, BaseModelMixin):
    u"""环境资源费用配置"""
    __tablename__ = "env_resource_fee"
    json_columns = [
        "internet_ip"
    ]
    env_id = Column(Integer, ForeignKey('env_info.id'), default=0)
    computer = Column(Float, default=0.00, info={"name": u"默认云主机费用(个)", "unit": u"元"})
    cpu = Column(Float, default=0.00, info={"name": u"默认CPU费用（个）", "unit": u"元"})
    memory = Column(Float, default=0.00, info={"name": u"默认内存费用（GB）", "unit": u"元"})
    disk = Column(Float, default=0.00, info={"name": u"默认云磁盘费用（个）", "unit": u"元"})
    disk_backup = Column(Float, default=0.00, info={"name": u"默认云磁盘备份费用（个）", "unit": u"元"})
    out_ip = Column(Float, default=0.00, info={"name": u"默认外部IP费用（个）", "unit": u"元"})
    snapshot = Column(Float, default=0.00, info={"name": u"默认快照费用（个）", "unit": u"元"})
    loadbalance = Column(Float, default=0.00, info={"name": u"默认负载均衡费用（个）", "unit": u"元"})
    internet_ip = Column(String, default="", info={"name": u"默认互联网IP选项", "unit": u"元"})
    internet_ip_ssl = Column(Float, default=0.00, info={"name": u"默认是否需要SSL卸载费用", "unit": u"元"})
    env = relationship("Env_Info", backref=backref("env_resource_fee", uselist=False))
                       #     cascade="all, delete, delete-orphan",
                       #     # single_parent=True,
                       #     passive_deletes=True
                       # ))


class Env_Resource_Value(BaseModel, BaseModelMixin):
    u"""环境资源推荐值（默认值）配置"""
    __tablename__ = "env_resource_value"
    env_id = Column(Integer, ForeignKey('env_info.id'), default=0)
    computer = Column(Integer, default=0, info={"name": u"默认云主机数量", "unit": u"个"})
    cpu = Column(Integer, default=0, info={"name": u"默认CPU数量", "unit": u"个"})
    memory = Column(Integer, default=0, info={"name": u"默认内存容量", "unit": u"GB"})
    disk = Column(Integer, default=0, info={"name": u"默认云磁盘数量", "unit": u"个"})
    disk_backup = Column(Integer, default=0, info={"name": u"默认云磁盘备份数量", "unit": u"个"})
    out_ip = Column(Integer, default=0, info={"name": u"默认外部IP", "unit": u"个"})
    snapshot = Column(Integer, default=0, info={"name": u"默认快照数量", "unit": u"个"})
    loadbalance = Column(Integer, default=0, info={"name": u"默认负载均衡数量", "unit": u"个"})
    internet_ip = Column(Integer, default=0, info={"name": u"默认互联网IP选项"})
    internet_ip_ssl = Column(Integer, default=0, info={"name": u"默认是否需要SSL卸载"})
    env = relationship("Env_Info", backref=backref("env_resource_value", uselist=False))
                       #     cascade="all, delete, delete-orphan",
                       #     # single_parent=True,
                       #     passive_deletes=True
                       # ))
