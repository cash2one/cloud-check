# -*- coding: utf-8 -*-

import simplejson
from tornado import gen
from collections import namedtuple
from scloud.config import logger, logThrown
from scloud.models.project import Pro_Info
from scloud.models.environment import Env_Info
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
        name = Pro_Info.__doc__,
        keyword = Pro_Info.__tablename__,
        keycode = 1001,
        ops = [op_view, op_insert, op_update, op_delete, op_check]
    ),
    _group(
        name = Env_Info.__doc__,
        keyword = Env_Info.__tablename__,  
        keycode = 1002,
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
        self.error = u"""the permission %s is not defined.""" % perm

    def __str__(self):
        return self.error


class PermissionError(Exception):
    def __init__(self, perm):
        self.error = u"""user do not have permission %s""" % perm

    def __str__(self):
        return self.error


def check_perms(perms):
    def func(method):
        def wrapper(self, *args, **kwargs):
            logger.info("perms: %s" % perms)
            sys_permissions = get_sys_group_ops()
            logger.info("--------------[sys_permissions]--------------")
            logger.info(sys_permissions)
            need_perms = perms.split(",")
            for perm in need_perms:
                try:
                    try:
                        keycode = sys_permissions[perm]
                    except KeyError:
                        raise PermissionDefinedError(perm)
                    # current_perms = self.current_perms
                    current_perms = self.current_user.current_perms
                    logger.info("--------------[current_perms]--------------")
                    logger.info(self.current_user.current_perms)
                    try:
                        current_keycode = current_perms[perm]
                    except KeyError:
                        raise PermissionError(perm)
                    if keycode == current_keycode:
                        return method(self, *args, **kwargs)
                    else:
                        raise PermissionError(perm)
                    return method(self, *args, **kwargs)
                except PermissionDefinedError as e:
                    headers = self.request.headers
                    x_requested_with = headers.get("X-Requested-With", "")
                    if self.pjax:
                        raise gen.Return(self.render("admin/error/401.html", content=u"Oops, The permission %s is not defined" % perm))
                    if x_requested_with == "XMLHttpRequest":
                        raise gen.Return(self.write(simplejson.dumps({
                            "return_code": -401,
                            "return_message": u"Oops, The permission %s is not defined" % perm
                            })))
                    else:
                        raise gen.Return(self.render("admin/error/401.html", content=u"Oops, The permission %s is not defined" % perm))
                except PermissionError(perm) as e:
                    logger.error(e)
                    headers = self.request.headers
                    x_requested_with = headers.get("X-Requested-With", "")
                    if self.pjax:
                        raise gen.Return(self.render("admin/error/401.html", content=u"Oops, The permission %s is not defined" % perm))
                    if x_requested_with == "XMLHttpRequest":
                        raise gen.Return(self.write(simplejson.dumps({
                            "return_code": -402,
                            "return_message": u"Oops, You don't have the permission %s" % perm
                            })))
                    else:
                        raise gen.Return(self.render("admin/error/401.html", perm=perm))
            return method(self, *args, **kwargs)
        return wrapper
    return func
