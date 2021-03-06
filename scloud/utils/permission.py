# -*- coding: utf-8 -*-

import simplejson
from tornado import gen
from collections import namedtuple
from scloud.config import logger, logThrown
from scloud.models.pt_user import PT_User, PT_Role
from scloud.models.project import (Pro_Info, Pro_Resource_Apply,
                                   Pro_User, Pro_Publish,
                                   Pro_Balance, Pro_Backup, Pro_Event)
from scloud.models.environment import Env_Info, Env_Internet_Ip_Types, Env_Resource_Fee, Env_Resource_Value
from tornado.util import ObjectDict

operate = namedtuple("operate", ["name", "keyword", "keycode"])
_group = namedtuple("group", ["name", "keyword", "keycode", "ops"])

op_view = operate(name=u"查询", keyword="view", keycode=101)
op_insert = operate(name=u"添加", keyword="insert", keycode=102)
op_update = operate(name=u"更新", keyword="update", keycode=103)
op_delete = operate(name=u"删除", keyword="delete", keycode=104)
op_check = operate(name=u"审核", keyword="check", keycode=105)

m = __import__("scloud.utils.permission", fromlist="scloud.utils.permission")
OP = [op for op in dir(m) if op.startswith("op_")]
OP = {m.__getattribute__(op).keycode: m.__getattribute__(op) for op in OP}
GROUP = ObjectDict()

sys_groups = [

    _group(
        name = PT_User.__doc__,
        keyword = PT_User.__tablename__,
        keycode = 1001,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
    _group(
        name = PT_Role.__doc__,
        keyword = PT_Role.__tablename__,
        keycode = 1002,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
    _group(
        name = Pro_Info.__doc__,
        keyword = Pro_Info.__tablename__,
        keycode = 1101,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Pro_Resource_Apply.__doc__,
        keyword = Pro_Resource_Apply.__tablename__,
        keycode = 1102,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Pro_User.__doc__,
        keyword = Pro_User.__tablename__,
        keycode = 1103,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Pro_Publish.__doc__,
        keyword = Pro_Publish.__tablename__,
        keycode = 1104,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Pro_Balance.__doc__,
        keyword = Pro_Balance.__tablename__,
        keycode = 1105,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Pro_Backup.__doc__,
        keyword = Pro_Backup.__tablename__,
        keycode = 1106,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Pro_Event.__doc__,
        keyword = Pro_Event.__tablename__,
        keycode = 1106,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Env_Info.__doc__,
        keyword = Env_Info.__tablename__,
        keycode = 1201,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
    _group(
        name = Env_Internet_Ip_Types.__doc__,
        keyword = Env_Internet_Ip_Types.__tablename__,
        keycode = 1202,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
    _group(
        name = Env_Resource_Fee.__doc__,
        keyword = Env_Resource_Fee.__tablename__,
        keycode = 1203,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
    _group(
        name = Env_Resource_Value.__doc__,
        keyword = Env_Resource_Value.__tablename__,
        keycode = 1204,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
]


def get_sys_group_ops():
    sys_group_ops = {}
    for group in sys_groups:
        for op in group.ops:
            sys_group_ops.update({"%s.%s" % (group.keyword, op.keyword): "%s.%s" % (group.keycode, op.keycode)})
    return sys_group_ops


def init_group():
    for g in sys_groups:
        GROUP[g.keycode] = g
        setattr(GROUP, g.keyword, g)
        # setattr(GROUP, str(g.keycode), g)

init_group()


class PermissionDefinedError(Exception):
    def __init__(self, perm):
        self.error = u"""the permission %s is undefined.""" % perm

    def __str__(self):
        return self.error


class PermissionError(Exception):
    def __init__(self, perm):
        self.error = u"""current user do not have the permission: %s""" % perm

    def __str__(self):
        return self.error


def check_perms(perms, _and=True):
    def func(method):
        def wrapper(self, *args, **kwargs):
            logger.info("perms: %s" % perms)
            sys_permissions = get_sys_group_ops()
            # logger.info("--------------[sys_permissions]--------------")
            # logger.info(sys_permissions)
            need_perms = [p.strip() for p in perms.split(",")]
            logger.info("_and = %s" % _and)
            logger.info("need_perms = %s" % need_perms)
            # for perm in need_perms:
            try:
                for perm in need_perms:
                    try:
                        keycode = sys_permissions[perm]
                    except KeyError:
                        raise PermissionDefinedError(perm)
                # logger.info(self.get_current_user())
                # logger.info(self.current_user)
                if self.current_user:
                    current_perms = self.current_user.current_perms

                    # logger.info("--------------[current_perms]--------------")
                    # logger.info(self.current_user.current_perms)
                    logger.info("---------------[checking perm]------------------")
                    # logger.info(perm)
                    if _and:
                        minus_result = set(need_perms) - set(current_perms.keys())
                        if len(minus_result) > 0:
                            perm = list(minus_result)[0]
                            raise PermissionError(perm)
                        else:
                            return method(self, *args, **kwargs)
                    else:
                        checking_result = [i for i in current_perms.keys() if i in need_perms]
                        if len(checking_result) > 0:
                            return method(self, *args, **kwargs)
                        else:
                            perm = need_perms[0]
                            raise PermissionError(perm)
                    # try:
                    #     current_keycode = current_perms[perm]
                    # except KeyError:
                    #     raise PermissionError(perm)
                    # if keycode == current_keycode:
                    #     return method(self, *args, **kwargs)
                    # else:
                    #     raise PermissionError(perm)
                    logger.info("%s check pass!" % need_perms)
                return method(self, *args, **kwargs)
            except PermissionDefinedError as e:
                headers = self.request.headers
                x_requested_with = headers.get("X-Requested-With", "")
                if self.pjax:
                    raise gen.Return(self.render("admin/error/403.html", error_message=u"Oops, The permission %s is not defined" % perm))
                if x_requested_with == "XMLHttpRequest":
                    raise gen.Return(self.write(simplejson.dumps({
                        "return_code": -403,
                        "return_message": u"Oops, The permission %s is not defined" % perm
                        })))
                else:
                    raise gen.Return(self.render("admin/error/403.html", error_message=u"Oops, The permission %s is not defined" % perm))
            except PermissionError as e:
                logger.error(e)
                headers = self.request.headers
                x_requested_with = headers.get("X-Requested-With", "")
                if self.pjax:
                    raise gen.Return(self.render("admin/error/403.html", error_message=e.__unicode__()))
                if x_requested_with == "XMLHttpRequest":
                    raise gen.Return(self.write(simplejson.dumps({
                        "return_code": -403,
                        "return_message": u"Oops, You don't have the permission %s" % perm
                        })))
                else:
                    raise gen.Return(self.render("admin/error/403.html", error_message=u"Oops, You don't have the permission %s" % perm))
            return method(self, *args, **kwargs)
        return wrapper
    return func
