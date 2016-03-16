# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_Role, PT_Role_Group_Ops
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.permission import sys_groups, GROUP, OP
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types


class PtRoleService(BaseService):

    @thrownException
    def get_list(self):
        logger.info("------[get_list]------")
        logger.info("self.params : %s" % self.params)
        search = self.params.get("search", "")
        or_conditions = or_()
        or_conditions.append(PT_Role.name.like("%" + search + "%"))
        or_conditions.append(PT_Role.desc.like("%" + search + "%"))
        or_conditions.append(PT_Role.remark.like("%" + search + "%"))
        pt_roles = self.db.query(
            PT_Role
        ).filter(
            or_conditions
        ).order_by(
            PT_Role.id.desc()
        ).all()
        return self.success(data=pt_roles)

    @thrownException
    def get_info(self):
        logger.info("------[get_info]------")
        logger.info(self.params)
        logger.info(self.handler.args)
        role_id = self.params.get("role_id")
        logger.info(role_id)
        pt_role = self.db.query(
            PT_Role
        ).filter(
            PT_Role.id == role_id
        ).first()
        if pt_role:
            data = {"pt_role": pt_role, "sys_groups": sys_groups}
            return self.success(data=data)
        else:
            return NotFoundError()

    @thrownException
    def get_role_group_ops(self):
        role_id = self.params.get("role_id")
        conditions = and_()
        conditions.append(PT_Role_Group_Ops.role_id == role_id)
        pt_role = self.db.query(
                PT_Role
            ).filter(
                PT_Role.id == role_id
            ).one()
        role_group_ops = self.db.query(
                PT_Role_Group_Ops
            ).filter(
                conditions
            ).order_by(
                PT_Role_Group_Ops.role_id.asc(),
                PT_Role_Group_Ops.group_keycode.asc(),
                PT_Role_Group_Ops.op_keycode.asc(),
            )
        role_group_ops = [r_g_o.as_dict(["group_keycode", "op_keycode"]) for r_g_o in role_group_ops]
        role_group_obj = {
                "%s.%s" % (
                    str(int(d["group_keycode"])), str(int(d["op_keycode"]))
                ): "%s.%s" % (
                    GROUP.get(int(d["group_keycode"])).keyword if GROUP.get(int(d["group_keycode"])) else "", OP[int(d["op_keycode"])].keyword
                ) for d in role_group_ops}
        data = {"pt_role": pt_role.as_dict(), "sys_groups": sys_groups, "role_group_obj": role_group_obj}
        return self.success(data=data)

    @thrownException
    def post_role_group_ops(self):
        role_id = self.params.get("role_id")
        group_ops = self.params.get("group_ops")
        result = self.get_role_group_ops()
        role_group_obj = result["data"]["role_group_obj"]
        role_group_op_list = role_group_obj.keys()
        logger.info("============================")
        logger.info(set(role_group_op_list))
        logger.info(set(group_ops))
        logger.info("============================")
        need_deletes = set(role_group_op_list) - set(group_ops)
        group_op_list = [(g, op) for g, op in [_str.split(".") for _str in group_ops]]
        need_delete_list = [(g, op) for g, op in [_str.split(".") for _str in need_deletes]]
        for g, op in group_op_list:
            instance, created = PT_Role_Group_Ops.get_or_create_obj(self.db,
                role_id = int(role_id),
                group_keycode = g,
                op_keycode = op
            )
        for g, op in need_delete_list:
            self.db.query(
                PT_Role_Group_Ops
            ).filter(
                PT_Role_Group_Ops.role_id == int(role_id),
                PT_Role_Group_Ops.group_keycode == g,
                PT_Role_Group_Ops.op_keycode == op
            ).delete()
        return self.success(data={"sys_groups": sys_groups})

    @thrownException
    def get_or_create(self):
        logger.info("------ [get_or_create] ------")
        name = self.params.get("name")
        desc = self.params.get("desc")
        remark = self.params.get("remark")
        role_info, created = PT_Role.get_or_create_obj(self.db,
            name = name,
            )
        role_info.desc = desc
        role_info.remark = remark
        self.db.add(role_info)
        return self.success()

    @thrownException
    def update_info(self):
        logger.info("------ [update_info] ------")
        role_id = self.params.get("role_id")
        name = self.params.get("name", "")
        desc = self.params.get("desc")
        remark = self.params.get("remark")
        role = self.db.query(
            PT_Role
        ).filter(
            PT_Role.id == role_id,
        ).first()
        if role:
            role.name = name
            role.desc = desc
            role.remark = remark
            self.db.add(role)
            return self.success(data={"is_success": True})
        else:
            return NotFoundError()

    @thrownException
    def delete_info(self):
        logger.info("------ [delete_info] ------")
        role_id = self.params.get("role_id")
        is_success = self.db.query(
                PT_Role
            ).filter(
                PT_Role.id == role_id,
            ).delete()
        return self.success(data={"is_success": is_success})

