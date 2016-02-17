# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.permission import GROUP, OP
from scloud.utils.error_code import ERROR


class LoginService(BaseService):

    @thrownException
    def do_login(self):
        username = self.params.get("username", "").strip()
        password = self.params.get("password", "").strip()
        if username == "":
            return self.failure(ERROR.username_empty_err)
        conditions = and_()
        or_conditions = or_()
        or_conditions.append(PT_User.username == username)
        or_conditions.append(PT_User.email == username)
        or_conditions.append(PT_User.mobile == username)
        conditions.append(or_conditions)
        conditions.append(PT_User.is_enable == 1)
        user_info = self.db.query(
            PT_User
        ).filter(
            conditions
        ).first()
        if user_info:
            if password == "":
                return self.failure(ERROR.password_empty_err)
            if user_info.password != password:
                return self.failure(ERROR.password_err)

            # LOGIN SUCCESS
            user_roles = user_info.user_roles
            current_perms = {}
            for user_role in user_roles:
                group_ops = user_role.role.group_ops
                for group_op in group_ops:
                    g_keyword = GROUP[group_op.group_keycode].keyword
                    op_keyword = OP[group_op.op_keycode].keyword
                    g_keycode = group_op.group_keycode
                    op_keycode = group_op.op_keycode
                    current_perms.update({"%s.%s" % (g_keyword, op_keyword): "%s.%s" % (g_keycode, op_keycode)})
            setattr(user_info, "current_perms", current_perms)
            result = self.success(data=user_info)
            user_info.last_login = datetime.now()
            self.db.add(user_info)
            #self.db.commit()
            return result
        else:
            return self.failure(ERROR.username_err)
