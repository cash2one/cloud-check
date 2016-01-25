# -*- coding: utf-8 -*-

from collections import namedtuple
from scloud.models.project import Pro_Info
from scloud.models.environment import Env_Info

op = namedtuple("op", ["name", "keyword", "keycode"])
group = namedtuple("group", ["name", "keyword", "keycode", "ops"])

op_view = op(name=u"查询", keyword="view", kecode=101)
op_insert = op(name=u"添加", keyword="insert", keycode=102)
op_update = op(name=u"更新", keyword="update", keycode=103)
op_delete = op(name=u"删除", keyword="delete", keycode=104)
op_check = op(name=u"删除", keyword="check", keycode=105)


groups = [
    group(
        name = Pro_Info.__doc__,
        keyword = Pro_Info.__tablename__,
        keycode = 1001,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
    group(
        name = Env_Info.__doc__,
        keyword = Env_Info.__tablename__,
        keycode = 1001,
        ops = [op_view, op_insert, op_update, op_delete]
    ),
]
