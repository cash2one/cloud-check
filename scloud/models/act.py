#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from sqlalchemy import Column, func
from sqlalchemy.types import Unicode, Integer
from scloud.models.base import BaseModel, BaseModelMixin, DataBaseService, IndexMark


class Act_History(BaseModel, BaseModelMixin):
    __tablename__ = "act_history"
    act_types = {
        0: IndexMark(value=u"未知操作", value_en="unkown operation", level="warning"),
        1: IndexMark(value=u"新增", value_en="insert", level="info"),
        2: IndexMark(value=u"修改", value_en="update", level="success"),
        3: IndexMark(value=u"删除", value_en="delete", level="danger"),
    }
    act_type = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    user_id = Column(Integer, default=0)


class Act_Todo(BaseModel, BaseModelMixin):
    __tablename__ = "act_todo"
    important_types = {
        0: IndexMark(value=u"普通", value_en="0", level="primary"),
        1: IndexMark(value=u"提示", value_en="1", level="info"),
        2: IndexMark(value=u"提醒", value_en="2", level="success"),
        2: IndexMark(value=u"重要", value_en="3", level="warning"),
        3: IndexMark(value=u"紧急", value_en="4", level="danger"),
    }
    important = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    from_user_id = Column(Integer, default=0)
    to_user_id = Column(Integer, default=0)
