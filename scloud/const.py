#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from collections import namedtuple
from tornado.util import ObjectDict

IndexMark = namedtuple("IndexMark", ["value", "value_en", "level"])
FeeMark = namedtuple("FeeMark", ["value", "value_en", "fee", "level"])
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

# Pro_Resource_Apply
# 资源申请状态
pro_resource_apply_status_types = {
    # 未申请状态，可修改，可删除，可提交
    None:ApplyMark(value=u"未申请", todo_value="待提交", act_value=u"申请", value_en="unknown", level="warning", bg_color="yellow"),
    -3:ApplyMark(value=u"已删除", todo_value="", act_value=u"", value_en="refused", level="danger", bg_color="red"),
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

# Pro_Resource_Apply
# 互联网宽带
pro_resource_apply_bandwidth_types = {
    # 0: IndexMark(value=u"0MB", value_en="mb0", level="primary"),
    1: IndexMark(value=u"2MB", value_en="mb2", level="default"),
    2: IndexMark(value=u"4MB", value_en="mb4", level="primary"),
    3: IndexMark(value=u"8MB", value_en="mb8", level="info"),
    4: IndexMark(value=u"16MB", value_en="mb16", level="success"),
}

RESOURCE_BANDWIDTH = ObjectDict()
def init_resource_bandwidth():
    for k, v in pro_resource_apply_bandwidth_types.items():
        setattr(RESOURCE_BANDWIDTH, v.value_en.upper(), k)
        setattr(RESOURCE_BANDWIDTH, v.value_en.lower(), v)
        RESOURCE_BANDWIDTH[k] = v
init_resource_bandwidth()

# pro_publish, pro_user, pro_backup, pro_balance
# 互联网发布、负载均衡、定期备份、权限申请状态
pro_tables_status_types = {
    # 未申请状态，可修改，可删除，可提交
    -2:ApplyMark(value=u"审核未通过", todo_value="待修改", act_value=u"保存", value_en="refused", level="danger", bg_color="red"),
    -1:ApplyMark(value=u"未提交", todo_value="待修改", act_value=u"保存", value_en="revoked", level="warning", bg_color="yellow"),
    0: ApplyMark(value=u"已提交", todo_value="受理中", act_value=u"保存", value_en="applied", level="info", bg_color="light-blue"),
    1: ApplyMark(value=u"已处理", todo_value="待确认", act_value=u"处理", value_en="checked", level="success", bg_color="light-blue"),
    2: ApplyMark(value=u"已确认", todo_value="已完成", act_value=u"确认", value_en="confirmed", level="success", bg_color="light-blue"),
}
STATUS_PRO_TABLES = ObjectDict()
def init_status_pro_tables():
    for k, v in pro_tables_status_types.items():
        setattr(STATUS_PRO_TABLES, v.value_en.upper(), k)
        setattr(STATUS_PRO_TABLES, v.value_en.lower(), v)
        STATUS_PRO_TABLES[k] = v
init_status_pro_tables()

# 互联网发布、负载均衡、定期备份、权限申请状态
priority_status_types = {
    # 未申请状态，可修改，可删除，可提交
    0: IndexMark(value=u"低", value_en="low", level="info"),
    1: IndexMark(value=u"中", value_en="normal", level="success"),
    2: IndexMark(value=u"高", value_en="high", level="warning"),
    3: IndexMark(value=u"紧急", value_en="urgent", level="danger"),
}
STATUS_PRIORITY = ObjectDict()
def init_status_priority():
    for k, v in priority_status_types.items():
        setattr(STATUS_PRIORITY, v.value_en.upper(), k)
        setattr(STATUS_PRIORITY, v.value_en.lower(), v)
        STATUS_PRIORITY[k] = v
init_status_priority()

# 互联网发布、负载均衡、定期备份、权限申请状态
loadbalance_plot_types = {
    # 未申请状态，可修改，可删除，可提交
    0: IndexMark(value=u"轮循", value_en="cycle", level="info"),
    1: IndexMark(value=u"最小连接数", value_en="minconnect", level="success"),
    2: IndexMark(value=u"主从", value_en="master", level="warning"),
    3: IndexMark(value=u"其他", value_en="other", level="danger"),
}
PLOT_LOADBALANCE = ObjectDict()
def init_loadbalance_plot():
    for k, v in loadbalance_plot_types.items():
        setattr(PLOT_LOADBALANCE, v.value_en.upper(), k)
        setattr(PLOT_LOADBALANCE, v.value_en.lower(), v)
        PLOT_LOADBALANCE[k] = v
init_loadbalance_plot()

# 互联网发布、负载均衡、定期备份、权限申请状态
loadbalance_health_types = {
    # 未申请状态，可修改，可删除，可提交
    0: IndexMark(value=u"HTTP", value_en="http", level="info"),
    1: IndexMark(value=u"TCP", value_en="tcp", level="success"),
    2: IndexMark(value=u"ICMP", value_en="icmp", level="warning"),
    3: IndexMark(value=u"其他", value_en="other", level="danger"),
}
LOADBALANCE_HEALTH = ObjectDict()
def init_loadbalance_health():
    for k, v in loadbalance_health_types.items():
        setattr(LOADBALANCE_HEALTH, v.value_en.upper(), k)
        setattr(LOADBALANCE_HEALTH, v.value_en.lower(), v)
        LOADBALANCE_HEALTH[k] = v
init_loadbalance_health()

# 是否
yesno_status_types = {
    1: IndexMark(value=u"是", value_en="yes", level="success"),
    0: IndexMark(value=u"否", value_en="no", level="warning"),
}
STATUS_YESNO = ObjectDict()
def init_status_yesno():
    for k, v in yesno_status_types.items():
        setattr(STATUS_YESNO, v.value_en.upper(), k)
        setattr(STATUS_YESNO, v.value_en.lower(), v)
        STATUS_YESNO[k] = v
init_status_yesno()

# （Pro_User）用户类型
pro_user_types = {
    1: IndexMark(value=u"dashboard", value_en="dashboard", level="success"),
    0: IndexMark(value=u"远程控制服务器", value_en="service", level="info"),
}
PRO_USER_TYPES = ObjectDict()
def init_pro_user_types():
    for k, v in pro_user_types.items():
        setattr(PRO_USER_TYPES, v.value_en.upper(), k)
        setattr(PRO_USER_TYPES, v.value_en.lower(), v)
        PRO_USER_TYPES[k] = v
init_pro_user_types()

from scloud.config import CONF
admin_emails = CONF("admin_emails")
# admin_emails = ["zhangpeng1@infohold.com.cn"]
