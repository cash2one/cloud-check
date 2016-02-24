#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from collections import namedtuple
from tornado.util import ObjectDict

IndexMark = namedtuple("IndexMark", ["value", "value_en", "level"])
ApplyMark = namedtuple("IndexMark", ["value", "todo_value", "act_value", "value_en", "level", "bg_color"])

# use in models
act_types = {
    0: IndexMark(value=u"未知操作", value_en="unkown operation", level="warning"),
    1: IndexMark(value=u"新增", value_en="insert", level="info"),
    2: IndexMark(value=u"修改", value_en="update", level="success"),
    3: IndexMark(value=u"删除", value_en="delete", level="danger"),
}

important_types = {
    0: IndexMark(value=u"普通", value_en="0", level="primary"),
    1: IndexMark(value=u"提示", value_en="1", level="info"),
    2: IndexMark(value=u"提醒", value_en="2", level="success"),
    3: IndexMark(value=u"重要", value_en="3", level="warning"),
    4: IndexMark(value=u"紧急", value_en="4", level="danger"),
}

# use in services
# scloud/async_services/svc_act.py
act_actions = {
    1: IndexMark(value=u"新增%s数据", value_en="", level="success"),
    2: IndexMark(value=u"更新%s数据", value_en="", level="warning"),
    3: IndexMark(value=u"删除%s数据", value_en="", level="danger"),
}

pro_resource_apply_status_types = {
    # 未申请状态，可修改，可删除，可提交
    None:ApplyMark(value=u"未申请", todo_value="待提交", act_value=u"申请", value_en="unknown", level="warning", bg_color="yellow"),
    -2:ApplyMark(value=u"审核未通过", todo_value="待修改", act_value=u"拒绝", value_en="refused", level="danger", bg_color="red"),
    -1:ApplyMark(value=u"已撤销", todo_value="待提交", act_value=u"撤销", value_en="revoked", level="warning", bg_color="yellow"),
    # 已提交状态，等待审核、等待缴费
    0: ApplyMark(value=u"已提交", todo_value="待审核", act_value=u"提交", value_en="applied", level="primary", bg_color="teal disabled"),
    1: ApplyMark(value=u"已审核", todo_value="待支付", act_value=u"审核", value_en="checked", level="info", bg_color="light-blue"),
    # 已支付状态，等待运行
    2: ApplyMark(value=u"完成支付", todo_value="待确认", act_value=u"支付", value_en="payed", level="success", bg_color="aqua"),
    3: ApplyMark(value=u"确认完成支付", todo_value="未启用", act_value=u"确认支付", value_en="confirmpayed", level="success", bg_color="aqua"),
    4: ApplyMark(value=u"运行中", todo_value="运行中", act_value=u"运行", value_en="started", level="danger", bg_color="red"),
    5: ApplyMark(value=u"已关闭", todo_value="未运行", act_value=u"关闭", value_en="closed", level="warning", bg_color="orange"),
}

STATUS_RESOURCE = ObjectDict()
def init_status_resource():
    for k, v in pro_resource_apply_status_types.items():
        setattr(STATUS_RESOURCE, v.value_en.upper(), k)
        setattr(STATUS_RESOURCE, v.value_en.lower(), v)
        STATUS_RESOURCE[k] = v
init_status_resource()

admin_emails = ["zhangpeng1@infohold.com.cn"]
