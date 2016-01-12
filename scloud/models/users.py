#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from myapp.shortcuts import *
from myapp.models import *

users = Table("users", metadata, schema='myapp', autoload=True)
class User(BaseModel):
    #__tablename__ = "users"
    __table__ = users
    #id = Column(Integer(10), autoincrement=True, primary_key=True)
    #username = Column(Unicode(11), server_default='')
    #password = Column(Unicode(32))
    #realname = Column(Unicode(10))
    #gender = Column(Integer(1))
    #mobile = Column(Unicode(15))
    #qq = Column(Unicode(15))
    #email = Column(Unicode(15))
    #birthday = Column(Date)
    #company = Column(Unicode(15))
    #address = Column(Unicode(15))

