# -*- coding: utf-8 -*-

from datetime import datetime
# from tornado import gen
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.const import STATUS_PRO_TABLES
from scloud.models.project import Pro_Balance 
import simplejson


class ApplyLoadBalance(BaseService):

    @thrownException
    def get_loadbalance(self):
        logger.info("------get_loadbalance------")
        pro_id = self.params.get("pro_id")
        pro_info = self.db.query(
            Pro_Info
        ).filter(
            Pro_Info.id == pro_id
        ).first()
        applies = pro_info.pro_resource_applies
        last_apply = applies[-1]
        loadbalance_plot = last_apply.loadbalance_plot
        # balance = self.db.query(
        #     Pro_Balance
        #     ).filter(
        #         Pro_Balance.pro_id == pro_id
        #     ).first()
        return self.success(data=loadbalance_plot)

    @thrownException
    def get_info(self):
        id = self.params.get("id")
        pro_balance = self.db.query(
            Pro_Balance
        ).filter(
            Pro_Balance.id == id
        ).first()
        return self.success(data=pro_balance)

    @thrownException
    def get_list(self):
        pro_id = self.params.get("pro_id")
        conditions = and_()
        if pro_id:
            conditions.append(Pro_Balance.pro_id == pro_id)
        pro_balance_list = self.db.query(
            Pro_Balance
        ).filter(
            conditions
        ).all()
        return self.success(data=pro_balance_list)

    @thrownException
    def do_loadbalance(self):
        pro_id = self.params.get("pro_id")
        res_apply_id = self.params.get("res_apply_id")
        member = self.params.get("members", "")
        members = simplejson.loads(member)
        g_plot_messages = []
        for mem in members:
            plot_messages = []
            port = mem['port']
            if not port:
                plot_messages.append(self.failure(ERROR.pro_balance_member_port_empty_err))
                g_plot_messages.append(self.failure(ERROR.pro_balance_member_port_empty_err))
            address = mem['address']
            if not address:
                plot_messages.append(self.failure(ERROR.pro_balance_member_address_empty_err))
                g_plot_messages.append(self.failure(ERROR.pro_balance_member_address_empty_err))
            mem["failures"] = plot_messages
        plot = self.params.get("plot", 0)
        health = self.params.get("health", 0)
        url = self.params.get("url")
        keyword = self.params.get("keyword")
        desc = self.params.get("desc", "")
        do_balance_info, created = Pro_Balance.get_or_create_obj(self.db, pro_id=pro_id, res_apply_id=res_apply_id)
        do_balance_info.plot = plot
        do_balance_info.health = health
        do_balance_info.url = url
        do_balance_info.keyword = keyword
        do_balance_info.desc = desc
        do_balance_info.user_id = self.handler.current_user.id
        if len(g_plot_messages) == 0:
            do_balance_info.status = 0
            do_balance_info.members = member
            self.db.add(do_balance_info)
            self.db.flush()
            return self.success(data=do_balance_info)
        else:
            do_balance_info.status = -1
            do_balance_info.members = simplejson.dumps(members)
            return self.failures(g_plot_messages, data=do_balance_info)
