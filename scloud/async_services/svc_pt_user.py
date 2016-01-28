#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import logger, thrownException
from scloud.celeryapp import celery
from scloud.models.pt_user import (PT_User, PT_Role, PT_User_Role, PT_Role_Group_Ops)
from scloud.utils.permission import GROUP, OP
from scloud.models.base import DataBaseService
from sqlalchemy import or_, and_
from pprint import pprint


@celery.task
@thrownException
def get_list(search=""):
    with DataBaseService({}) as svc:
        or_conditions = or_()
        or_conditions.append(PT_User.username.like("%" + search + "%"))
        pt_users = svc.db.query(
            PT_User
        ).filter(
            or_conditions
        ).order_by(
            PT_User.id.desc()
        ).all()
        pt_users = [i.as_dict() for i in pt_users]
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": pt_users
        }
    return data


@celery.task
@thrownException
def get_info(user_id):
    with DataBaseService({}) as svc:
        pt_user = svc.db.query(
            PT_User
        ).filter(
            PT_User.id == user_id
        ).one()
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"pt_user": pt_user.as_dict()}
        }
    return data


@celery.task
@thrownException
def get_or_create(username, password):
    """
        添加管理用户
    """
    user_instance, created = PT_User.get_or_create(username=username)
    user_instance.password = password
    with DataBaseService({}) as svc:
        svc.db.add(user_instance)
        user_info = svc.db.query(
            PT_User
        ).filter(
            PT_User.username == username
        ).first()
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"pt_user": user_info.as_dict()}
        }
    return data


@celery.task
@thrownException
def update_info(user_id, username=u"", password=u""):
    # import time
    # time.sleep(60)
    with DataBaseService({}) as svc:
        user_filter = svc.db.query(
            PT_User
        ).filter(
            PT_User.id == user_id,
        )
        pprint(str(user_filter))
        user = user_filter.one()
        user.username = username
        user.password = password
        svc.db.add(user)
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"pt_user": user.as_dict()}
        }
    return data


@celery.task
@thrownException
def delete_info(user_id):
    with DataBaseService({}) as svc:
        is_success = svc.db.query(
            PT_User
        ).filter(
            PT_User.id == user_id,
        ).delete()
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"success": is_success}
        }
    return data


@celery.task
@thrownException
def get_user_roles(user_id):
    conditions = and_()
    conditions.append(PT_User_Role.user_id == user_id)
    with DataBaseService({}) as svc:
        role_list = svc.db.query(
            PT_Role
        ).filter(
            PT_Role.is_enable == 1
        ).order_by(
            PT_Role.id.asc(),
        )
        roles = [r.as_dict() for r in role_list]
        role_obj = {}
        user_roles = svc.db.query(
            PT_User_Role
        ).filter(
            PT_User_Role.user_id == user_id
        ).all()
        role_group_obj = {}
        for user_role in user_roles:
            role_group_ops = user_role.role.group_ops
            # role_group_ops = svc.db.query(
            #     PT_Role_Group_Ops
            # ).outerjoin(
            #     PT_User_Role, PT_Role_Group_Ops.role_id == PT_User_Role.role_id
            # ).filter(
            #     conditions
            # ).order_by(
            #     PT_Role_Group_Ops.role_id.asc(),
            #     PT_Role_Group_Ops.group_keycode.asc(),
            #     PT_Role_Group_Ops.op_keycode.asc(),
            # )
            role_group_ops = [r_g_o.as_dict(["role_id", "group_keycode", "op_keycode"]) for r_g_o in role_group_ops]
            # pprint(role_group_ops)
            role_group_obj.update({
                "%s.%s" % (
                    str(int(d["group_keycode"])), str(int(d["op_keycode"]))
                ): "%s.%s" % (
                    GROUP[int(d["group_keycode"])].keyword, OP[int(d["op_keycode"])].keyword
                ) for d in role_group_ops})
            role_obj.update({user_role.role.id: role_group_obj})
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": {"roles": roles, "role_obj": role_obj, "role_group_obj": role_group_obj}
        }
    return data


@celery.task
@thrownException
def post_user_roles(user_id, role_ids):
    result = get_user_roles(user_id)
    user_role_obj = result["data"]["role_obj"]
    user_role_list = [str(i) for i in user_role_obj.keys()]
    # logger.info("============================")
    # logger.info(set(role_group_op_list))
    # logger.info(set(group_ops))
    # logger.info("============================")
    need_deletes = set(user_role_list) - set(role_ids)
    logger.info(need_deletes)
    # role_list = [(g, op) for g, op in [_str.split(".") for _str in role_ids]]
    # need_delete_list = [(g, op) for g, op in [_str.split(".") for _str in need_deletes]]
    for role_id in role_ids:
        instance, created = PT_User_Role.get_or_create(
            user_id = int(user_id),
            role_id = int(role_id),
        )
    with DataBaseService({}) as svc:
        for role_id in need_deletes:
            svc.db.query(
                PT_User_Role
            ).filter(
                PT_User_Role.user_id == int(user_id),
                PT_User_Role.role_id == int(role_id)
            ).delete()
    data = {
        "return_code": 0,
        "return_message": u"",
        "data": {"roles": result["data"]["roles"]}
    }
    return data


# @celery.task
# def get_group_list(kwargs):
#     """
#         获取用户所属权限组
#     """
#     with DataBaseService(kwargs) as svc:
#         groups = svc.db.query(
#             PT_User_Group_Permissions,
#             PT_Group,
#         ) \
#             .join(PT_Group, PT_Group.id == PT_User_Group_Permissions.group_id) \
#             .filter(PT_User_Group_Permissions.user_id == kwargs["id"]) \
#             .group_by(PT_Group.id) \
#             .all()
#     return groups

# @celery.task
# def get_perm_list(kwargs):
#     """
#         获取用户所属权限组所有操作权限
#     """
#     with DataBaseService(kwargs) as svc:
#         permissions = svc.db.query(
#                 PT_User_Group_Permissions,
#                 PT_Group,
#                 PT_Permission
#             ).join(
#                 PT_Group, PT_Group.id == PT_User_Group_Permissions.group_id
#             ).join(
#                 PT_Permission, PT_Permission.id == PT_User_Group_Permissions.perm_id
#             ).order_by(
#                 PT_User_Group_Permissions.group_id,
#                 PT_User_Group_Permissions.perm_id
#             ).filter(
#                 PT_User_Group_Permissions.user_id == kwargs["id"]
#             # ).fetchAll(
#             #     cache, key, CACHE("TIMEOUT.MINUTE") * 2
#             # )
#             .all()
#     return permissions

# @celery.task
# def get_perms(kwargs):
#     """
#         获取用户所属权限组所有操作权限
#     """
#     permissions = get_perm_list(kwargs)
#     perms = {
#         "%s.%s" % (g.keyword, p.keyword): "%s.%s" % (g.keycode, p.keycode)
#         for u_g_p, g, p in permissions
#     }
#     return perms

# @celery.task
# def has_perms(perm_list, kwargs):
#     """
#         查看用户是否有指定定权限
#     """
#     current_perms = get_perms(kwargs)
#     for perm in perm_list:
#         if current_perms.get(perm, None) == None:
#             return False
#     return True

# @celery.task
# def get_all_pt_user():
#     """
#         获取所有用户
#     """
#     with DataBaseService({}) as svc:
#         pt_users = svc.db.query(PT_User).all()
#     return pt_users

# @celery.task
# def change_user_status(user_id, user_status):
#     with DataBaseService({}) as svc:
#         is_success = svc.db.query(
#             PT_User
#         ).filter(
#             PT_User.id == user_id
#         ).update(
#             {
#                 PT_User.is_enable: user_status,
#             }
#         )
#     return is_success
