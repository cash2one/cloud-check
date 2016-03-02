# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import (PT_User, PT_Role, PT_User_Role, PT_Role_Group_Ops)
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.permission import sys_groups, GROUP, OP
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types


class PtUserService(BaseService):

    @thrownException
    def get_list(self):
        logger.info("------[get_list]------")
        search = self.params.get("search", "")
        or_conditions = or_()
        or_conditions.append(PT_User.username.like("%" + search + "%"))
        or_conditions.append(PT_User.email.like("%" + search + "%"))
        or_conditions.append(PT_User.mobile.like("%" + search + "%"))
        pt_users = self.db.query(
            PT_User
        ).filter(
            or_conditions
        ).order_by(
            PT_User.id.desc()
        ).all()
        return self.success(data=pt_users)

    @thrownException
    def get_info(self):
        logger.info("------[get_info]------")
        logger.info(self.params)
        logger.info(self.handler.args)
        user_id = self.params.get("user_id")
        logger.info(user_id)
        pt_user = self.db.query(
            PT_User
        ).filter(
            PT_User.id == user_id
        ).first()
        if pt_user:
            data = {"pt_user": pt_user}
            return self.success(data=data)
        else:
            return NotFoundError()

    @thrownException
    def get_or_create(self):
        logger.info("------ [get_or_create] ------")
        username = self.params.get("username", "")
        email = self.params.get("email", "")
        mobile = self.params.get("mobile", "")
        password = self.params.get("password", "")
        user_instance, created = PT_User.get_or_create(username=username, email=email, mobile=mobile)
        user_instance.password = password
        self.db.add(user_instance)
        user_info = self.db.query(
            PT_User
        ).filter(
            PT_User.username == username
        ).first()
        data = {"pt_user": user_info}
        return self.success(data=data)

    @thrownException
    def update_info(self):
        logger.info("------ [update_info] ------")
        user_id = self.params.get("user_id")
        username = self.params.get("username", "")
        email = self.params.get("email", "")
        mobile = self.params.get("mobile", "")
        password = self.params.get("password")
        user_filter = self.db.query(
            PT_User
        ).filter(
            PT_User.id == user_id,
        )
        user = user_filter.first()
        if user:
            user.username = username
            user.email = email
            user.mobile = mobile
            if password:
                user.password = password
            self.db.add(user)
            return self.success(data={"pt_user": user})
        else:
            return NotFoundError()

    @thrownException
    def delete_info(self):
        logger.info("------ [delete_info] ------")
        user_id = self.params.get("user_id")
        is_success = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id,
            ).delete()
        return self.success(data={"is_success": is_success})

    @thrownException
    def get_user_roles(self):
        user_id = self.params.get("user_id")
        conditions = and_()
        conditions.append(PT_User_Role.user_id == user_id)
        role_list = self.db.query(
            PT_Role
        ).filter(
            PT_Role.is_enable == 1
        ).order_by(
            PT_Role.id.asc(),
        )
        roles = [r.as_dict() for r in role_list]
        role_obj = {}
        user_roles = self.db.query(
            PT_User_Role
        ).filter(
            PT_User_Role.user_id == user_id
        ).all()
        role_group_obj = {}
        for user_role in user_roles:
            role_group_ops = user_role.role.group_ops
            role_group_ops = [r_g_o.as_dict(["role_id", "group_keycode", "op_keycode"]) for r_g_o in role_group_ops]
            role_group_obj.update({
                "%s.%s" % (
                    str(int(d["group_keycode"])), str(int(d["op_keycode"]))
                ): "%s.%s" % (
                    GROUP[int(d["group_keycode"])].keyword, OP[int(d["op_keycode"])].keyword
                ) for d in role_group_ops})
            role_obj.update({user_role.role.id: role_group_obj})
        data = {"roles": roles, "role_obj": role_obj, "role_group_obj": role_group_obj}
        return self.success(data=data)

    @thrownException
    def post_user_roles(self):
        user_id = self.params.get("user_id")
        role_ids = self.params.get("role_ids")
        result = self.get_user_roles()
        user_role_obj = result["data"]["role_obj"]
        user_role_list = [str(i) for i in user_role_obj.keys()]
        need_deletes = set(user_role_list) - set(role_ids)
        logger.info(need_deletes)
        for role_id in role_ids:
            instance, created = PT_User_Role.get_or_create(
                user_id = int(user_id),
                role_id = int(role_id),
            )
        for role_id in need_deletes:
            self.db.query(
                PT_User_Role
            ).filter(
                PT_User_Role.user_id == int(user_id),
                PT_User_Role.role_id == int(role_id)
            ).delete()
        data = {"roles": result["data"]["roles"]}
        return self.success(data=data)
