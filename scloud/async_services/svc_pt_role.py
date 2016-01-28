#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import logger, thrownException
from scloud.celeryapp import celery
from scloud.utils.permission import sys_groups, GROUP, OP
from scloud.models.base import DataBaseService
from scloud.models.pt_user import PT_Role, PT_Role_Group_Ops
from sqlalchemy import or_, and_


@celery.task
@thrownException
def get_list(search=""):
    with DataBaseService({}) as svc:
        or_conditions = or_()
        or_conditions.append(PT_Role.name.like("%" + search + "%"))
        or_conditions.append(PT_Role.desc.like("%" + search + "%"))
        or_conditions.append(PT_Role.remark.like("%" + search + "%"))
        pt_roles = svc.db.query(
            PT_Role
        ).filter(
            or_conditions
        ).order_by(
            PT_Role.id.desc()
        ).all()
        pt_roles = [i.as_dict() for i in pt_roles]
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": pt_roles
        }
    return data


@celery.task
@thrownException
def get_info(role_id):
    with DataBaseService({}) as svc:
        pt_role = svc.db.query(
            PT_Role
        ).filter(
            PT_Role.id == role_id
        ).one()
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"pt_role": pt_role.as_dict(), "sys_groups": sys_groups}
        }
    return data


@celery.task
@thrownException
def get_role_group_ops(role_id):
    conditions = and_()
    conditions.append(PT_Role_Group_Ops.role_id == role_id)
    with DataBaseService({}) as svc:
        role_group_ops = svc.db.query(
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
                GROUP[int(d["group_keycode"])].keyword, OP[int(d["op_keycode"])].keyword
            ) for d in role_group_ops}
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"sys_groups": sys_groups, "role_group_obj": role_group_obj}
        }
    print data
    return data


@celery.task
@thrownException
def post_role_group_ops(role_id, group_ops):
    result = get_role_group_ops(role_id)
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
        instance, created = PT_Role_Group_Ops.get_or_create(
            role_id = int(role_id),
            group_keycode = g,
            op_keycode = op
        )
    with DataBaseService({}) as svc:
        for g, op in need_delete_list:
            svc.db.query(
                PT_Role_Group_Ops
            ).filter(
                PT_Role_Group_Ops.role_id == int(role_id),
                PT_Role_Group_Ops.group_keycode == g,
                PT_Role_Group_Ops.op_keycode == op
            ).delete()
    data = {
        "return_code": 0,
        "return_message": u"",
        "data": {"sys_groups": sys_groups}
    }
    return data


@celery.task
@thrownException
def get_or_create(name, desc=u"", remark=u""):
    role_info, created = PT_Role.get_or_create(
        name = name,
        )
    role_info.desc = desc
    role_info.remark = remark
    with DataBaseService({}) as svc:
        svc.db.add(role_info)
    data = {
            "return_code": 0,
            "return_message": u"",
            "data": role_info.as_dict()
        }
    return data


@celery.task
@thrownException
def update_info(role_id, name=u"", desc=u"", remark=u""):
    with DataBaseService({}) as svc:
        role = svc.db.query(
            PT_Role
        ).filter(
            PT_Role.id == role_id,
        ).one()
        role.name = name
        role.desc = desc
        role.remark = remark
        svc.db.add(role)
    data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"pt_role": role.as_dict(), "sys_groups": sys_groups}
        }
    return data


@celery.task
@thrownException
def delete_info(role_id):
    with DataBaseService({}) as svc:
        is_success = svc.db.query(
            PT_Role
        ).filter(
            PT_Role.id == role_id,
        ).delete()
    data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"is_success": is_success}
        }
    return data
