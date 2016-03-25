# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types
from scloud.models.project import Pro_Balance 
import simplejson

class ApplyBalance(BaseService):
    @thrownException
    def get_balance(self):
        pro_id = self.params.get("pro_id")
        balance = self.db.query(
            Pro_Balance
            ).filter(
                Pro_Balance.pro_id == pro_id
            ).first()
        return self.success(data = balance)


    @thrownException
    def do_balance(self):
        pro_id = self.params.get("pro_id")
        res_apply_id = self.params.get("res_apply_id")
        member = self.params.get("balance_str")
        members = simplejson.loads(member)
        for mem in members:
            port = mem['port']
            if not port:
                return self.failure(ERROR.pro_balance_member_port_empty_err)
            address = mem['address']
            if not address:
                return self.failure(ERROR.pro_balance_member_address_empty_err)
        plot = self.params.get("plot", 0)    
        health = self.params.get("health", 0)
        url = self.params.get("url")
        keyword = self.params.get("keyword")
        desc = self.params.get("desc")
        do_balance_info, created = Pro_Balance.get_or_create_obj(self.db, pro_id=pro_id)
        do_balance_info.pro_id = pro_id
        do_balance_info.res_apply_id = res_apply_id
        do_balance_info.members = member
        do_balance_info.plot = plot
        do_balance_info.health = health
        do_balance_info.url = url
        do_balance_info.keyword = keyword
        do_balance_info.desc = desc
        self.db.add(do_balance_info)
        return self.success(data=do_balance_info)
        


        






