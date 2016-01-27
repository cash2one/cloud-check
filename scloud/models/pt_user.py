#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.models.base import BaseModel, BaseModelMixin
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Unicode, Integer, DateTime


# 用户表
class PT_User(BaseModel, BaseModelMixin):
    u"""用户"""
    __tablename__ = "pt_user"
    username = Column(Unicode, default=u'')
    password = Column(Unicode, default=u'')
    last_login = Column(DateTime, default=func.now())
    is_enable = Column(Integer, default=1)


class PT_Role(BaseModel, BaseModelMixin):
    u"""角色"""
    __tablename__ = "pt_role"
    name = Column(Unicode, default=u'')
    desc = Column(Unicode, default=u'')
    remark = Column(Unicode, default=u'')
    is_enable = Column(Integer, default=1)


class PT_Group(BaseModel, BaseModelMixin):
    u"""权限组"""
    __tablename__ = "pt_group"
    name = Column(Unicode, default=u'')
    keyword = Column(Unicode, default=u'')
    keycode = Column(Unicode, default=u'')
    is_enable = Column(Unicode, default=1)


class PT_Perm(BaseModel, BaseModelMixin):
    u"""操作"""
    __tablename__ = "pt_perm"
    name = Column(Unicode, default=u'')
    keyword = Column(Unicode, default=u'')
    keycode = Column(Unicode, default=u'')
    is_enable = Column(Unicode, default=1)


class PT_Group_Perms(BaseModel, BaseModelMixin):
    u"""操作权限管理"""
    __tablename__ = "pt_group_perms"
    group_id = Column(Integer, ForeignKey("pt_group.id"), default=0)
    perm_id = Column(Integer, default=0)
    group = relationship("PT_Group", backref="perms")


# 角色-权限组-操作权限表
class PT_Role_Group_Ops(BaseModel, BaseModelMixin):
    u"""角色权限管理"""
    __tablename__ = "pt_role_group_ops"
    role_id = Column(Integer, ForeignKey("pt_role.id"), default=0)
    group_keycode = Column(Integer, ForeignKey("pt_group_perms.id"), default=0)
    op_keycode = Column(Integer, ForeignKey("pt_group_perms.id"), default=0)


# 用户-角色表
class PT_User_Role(BaseModel, BaseModelMixin):
    u"""用户角色管理"""
    __tablename__ = "pt_user_role"
    role_id = Column(Integer, ForeignKey("pt_role.id"), default=0)
    user_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    role = relationship("PT_Role", backref="users")
    user = relationship("PT_User", backref="roles")
