#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from scloud.models.base import BaseModel, BaseModelMixin


class Act_History(BaseModel, BaseModelMixin):
    __tablename__ = "act_history"
    act_type = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    user_id = Column(Integer, default=0)


class Act_Todo(BaseModel, BaseModelMixin):
    __tablename__ = "act_todo"
    important = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')
    from_user_id = Column(Integer, default=0)
    to_user_id = Column(Integer, default=0)
