#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import String, INT, Integer, Unicode, Date, DateTime
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

