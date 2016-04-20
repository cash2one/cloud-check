# -*- coding: utf-8 -*-

from datetime import datetime
# from tornado import gen
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
# from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.const import STATUS_PRO_TABLES
from scloud.models.project import Pro_User 
from scloud.models.pt_user import PT_User


class ProUserService(BaseService):

    @thrownException
    def do_pro_user(self):
        try:
            pro_id = int(self.params.get("pro_id"))
        except:
            return self.failure(ERROR.pro_name_empty_err)
        username = self.params.get("username")
        email = self.params.get("email")
        is_enable = int(self.params.get("is_enable", 1))
        use_vpn = int(self.params.get("use_vpn", 0))
        if not pro_id:
            return self.failure(ERROR.pro_name_empty_err)
        if not username:
            return self.failure(ERROR.username_empty_err)
        if not email:
            return self.failure(ERROR.email_empty_err)
        if self.email_check(email) == 0:
            return self.failure(ERROR.email_format_err) 
        user_id = self.params.get("user_id")
        if user_id:
            pro_user = self.db.query(
                Pro_User
            ).filter(
                Pro_User.id == user_id
            ).first()
        else:
            pro_user = Pro_User()
        pro_user.pro_id = pro_id
        pro_user.username = username
        pro_user.email = email
        pro_user.is_enable = is_enable
        pro_user.use_vpn = use_vpn
        pro_user.user_id = self.handler.current_user.id
        self.db.add(pro_user)
        self.db.flush()
        return self.success(data=pro_user)

    @thrownException
    def get_list(self):
        pro_id = int(self.params.get("pro_id", 0))
        search = self.params.get("search", '')
        conditions = and_()
        user_id = self.params.get("user_id")
        if user_id:
            pt_user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id
            ).first()
            if pt_user and not pt_user.imchecker:
                conditions.append(Pro_User.user_id == user_id)
        if pro_id:
            conditions.append(Pro_User.pro_id == pro_id)
        if search:
            conditions.append(Pro_User.username.like('%' + search + '%'))
        pro_users = self.db.query(
            Pro_User
        ).filter(
            conditions
        ).order_by(Pro_User.id.desc()).all()
        # logger.info([i.as_dict() for i in pro_users])
        return self.success(data=pro_users)

    @thrownException
    def get_info(self):
        user_id = self.params.get("id")
        if user_id:
            pro_user = self.db.query(
                Pro_User
            ).filter(
                Pro_User.id == user_id    
            ).first()
            return self.success(data=pro_user)
        else:
            return self.failure(ERROR.not_found_err)

    @thrownException
    def do_del_pro_user(self):
        user_id_list = self.params.get("user_id_list")
        for user_id in user_id_list:
            pro_user = self.db.query(
                Pro_User
            ).filter(
                Pro_User.id == user_id    
            ).first()
            self.db.delete(pro_user)
            self.db.flush()
        return self.success(data=None)
