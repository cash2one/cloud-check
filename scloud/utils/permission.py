# -*- coding: utf-8 -*-

from collections import namedtuple
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


def init_group():

    for g in sys_groups:
        GROUP[g.keycode] = g
        setattr(GROUP, g.keyword, g)
        # setattr(GROUP, str(g.keycode), g)

init_group()
