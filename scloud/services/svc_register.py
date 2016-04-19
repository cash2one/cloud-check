# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User, PT_User_Role
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.permission import GROUP, OP
from scloud.utils.error_code import ERROR
import re 

class RegisterService(BaseService):
    @thrownException
    def email_check(self,email):
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return 1
        return 0

    @thrownException
    def do_register(self):
        captcha = self.params.get("captcha")
        if not captcha:
            return self.failure(ERROR.captcha_empty_err)
        if not self.handler.session.get("captcha"):
            return self.failure(ERROR.captcha_expired_err)
        if captcha != self.handler.session.get("captcha"):
            return self.failure(ERROR.captcha_err)
        email = self.params.get("email", "").strip()
        username = self.params.get("username", "").strip()
        mobile = self.params.get("mobile", "").strip().replace(' ', '')
        password = self.params.get("password", "").strip()
        if email == "":
            return self.failure(ERROR.email_empty_err)
        if self.email_check(email) == 0:
            return self.failure(ERROR.email_format_err) 
        if mobile == "":
            return self.failure(ERROR.mobile_empty_err)
        regex = re.compile(r'1\d{10}', re.IGNORECASE)
        match_result = re.match(regex, mobile)
        if not match_result:
            return self.failure(ERROR.mobile_format_err)
        if password == "":
            return self.failure(ERROR.password_empty_err)
        pt_user = self.db.query(
           PT_User 
        ).filter(
            PT_User.email == email
        ).first()
        if pt_user:
            return self.failure(ERROR.email_duplicate_err) 
        pt_user = self.db.query(
           PT_User 
        ).filter(
            PT_User.username == username
        ).first()
        if pt_user:
            return self.failure(ERROR.username_duplicate_err) 

        pt_user = self.db.query(
           PT_User 
        ).filter(
            PT_User.mobile == mobile
        ).first()
        if pt_user:
            return self.failure(ERROR.mobile_duplicate_err) 

        instance, created = PT_User.get_or_create_obj(self.db, email=email, mobile=mobile, password=password)
        PT_User_Role.get_or_create_obj(self.db, user_id=instance.id, role_id=2)
        conditions = and_()
        conditions.append(PT_User.id == instance.id)
        conditions.append(PT_User.is_enable == 1)
        user_info = self.db.query(
            PT_User
        ).filter(
            conditions
        ).first()
        if user_info:
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
            self.db.flush()
            return result
        else:
            return self.failure(ERROR.username_err)
