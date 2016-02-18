#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from collections import namedtuple

IndexMark = namedtuple("IndexMark", ["value", "value_en", "level"])
ApplyMark = namedtuple("IndexMark", ["value", "todo_value", "value_en", "level", "bg_color"])

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
    None:ApplyMark(value=u"未申请", todo_value="待提交", value_en="unkown", level="warning", bg_color="yellow"),
    -2:ApplyMark(value=u"审核未通过", todo_value="待修改", value_en="checked", level="danger", bg_color="red"),
    -1:ApplyMark(value=u"已撤销", todo_value="待提交", value_en="revoked", level="warning", bg_color="yellow"),
    # 已提交状态，等待审核、等待缴费
    0: ApplyMark(value=u"已提交", todo_value="待审核", value_en="applied", level="default", bg_color="teal disabled"),
    1: ApplyMark(value=u"已审核", todo_value="待支付", value_en="checked", level="primary", bg_color="light-blue"),
    # 已支付状态，等待运行
    2: ApplyMark(value=u"已支付", todo_value="未启用", value_en="payed", level="info", bg_color="aqua"),
    3: ApplyMark(value=u"运行中", todo_value="运行中", value_en="started", level="success", bg_color="green"),
    4: ApplyMark(value=u"已关闭", todo_value="未运行", value_en="closed", level="warning", bg_color="orange"),
}

