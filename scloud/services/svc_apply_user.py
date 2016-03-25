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
from scloud.models.project import Pro_User 


class ProUserService(BaseService):

    @thrownException
    def do_pro_user(self):
        pro_id = int(self.params.get("pro_id"))
        username = self.params.get("username")
        email = self.params.get("email")
        is_enable = int(self.params.get("is_enable", 1))
        use_vpn = int(self.params.get("use_vpn", 0))
        if not username:
            return self.failure(ERROR.username_empty_err)
        if not email:
            return self.failure(ERROR.email_empty_err)
        pro_user = Pro_User()
        pro_user.pro_id = pro_id
        pro_user.username = username
        pro_user.email = email
        pro_user.is_enable = is_enable
        pro_user.use_vpn = use_vpn
        self.db.add(pro_user)
        self.db.flush()
        return self.success(data=pro_user)

    @thrownException
    def get_list(self):
        pro_id = int(self.params.get("pro_id"))
        pro_users = self.db.query(
            Pro_User
        ).filter(
            Pro_User.pro_id == pro_id    
        ).all()
        return self.success(data=pro_users)

