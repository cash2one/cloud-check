#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relationship, backref
from scloud.models.base import BaseModel, BaseModelMixin
from scloud.models.project import Pro_Info, Pro_Resource_Apply


class Act_Pro_History(BaseModel, BaseModelMixin):
    u"""数据操作历史表"""
    __tablename__ = "act_pro_history"
    pro_id = Column(Integer, ForeignKey("pro_info.id"), default=0)
    res_apply_id = Column(Integer, ForeignKey("pro_resource_apply.id"), default=0)
    status = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    user_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    checker_id = Column(Integer, ForeignKey("pt_user.id"), default=0)
    pro = relationship("Pro_Info", backref="act_pro_histories")
    # user = relationship("PT_User", backref="act_pro_histories")
    user = relationship("PT_User", foreign_keys=[user_id], backref="act_pro_histories")
    checker = relationship("PT_User", foreign_keys=[checker_id], backref="checked_act_pro_histories")
    res_apply = relationship("Pro_Resource_Apply", backref=backref("act_pro_histories", order_by="Act_Pro_History.create_time"))


class Act_History(BaseModel, BaseModelMixin):
    u"""数据操作历史表"""
    __tablename__ = "act_history"
    record_id = Column(Integer, default=0)
    record_table = Column(Unicode, default=u'')
    act_type = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    user_id = Column(Integer, default=0)


class Act_Todo(BaseModel, BaseModelMixin):
    u"""TODO信息"""
    __tablename__ = "act_todo"
    important = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    from_user_id = Column(Integer, default=0)
    to_user_id = Column(Integer, default=0)
