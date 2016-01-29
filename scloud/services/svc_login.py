# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.permission import GROUP, OP


class LoginService(BaseService):

    @thrownException
    def do_login(self):
        username = self.params.get("username", "").strip()
        password = self.params.get("password", "").strip()
        if username == "":
            return self.failure(-100002, u"用户名不能为空")
        conditions = and_()
        conditions.append(PT_User.username == username)
        conditions.append(PT_User.is_enable == 1)
        user_info = self.db.query(
            PT_User
        ).filter(
            conditions
        ).first()
        if user_info:
            if password == "":
                return self.failure(-100003, u"密码不能为空")
            if user_info.password != password:
                return self.failure(-100004, u"密码错误")

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
            self.db.commit()
            return result
        else:
            return self.failure(-100001, u"该用户不存在")
