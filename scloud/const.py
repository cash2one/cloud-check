#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from collections import namedtuple

IndexMark = namedtuple("IndexMark", ["value", "value_en", "level"])

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
    2: IndexMark(value=u"重要", value_en="3", level="warning"),
    3: IndexMark(value=u"紧急", value_en="4", level="danger"),
}

# use in services
# scloud/async_services/svc_act.py
act_actions = {
    1: IndexMark(value=u"新增%s数据", value_en="", level="success"),
    2: IndexMark(value=u"更新%s数据", value_en="", level="warning"),
    3: IndexMark(value=u"删除%s数据", value_en="", level="danger"),
}
