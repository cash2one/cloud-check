#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from torweb.urls import url
from scloud.const import act_actions
from scloud.config import logger
from scloud.handlers import Handler
from scloud.models.pt_user import PT_Perm
from tornado.web import asynchronous
from tornado import gen
from scloud.async_services import svc_pt_permission


@url("/pt_perm", name="pt_perm", active="pt_perm")
class PT_Perm_Handler(Handler):
    u"""操作权限管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        search = self.args.get("search", "")
        response = yield gen.Task(svc_pt_permission.get_list.apply_async, args=[search])
        data = {"result": response.result}
        raise gen.Return(self.render("admin/pt_perm/index.html", **data))

    @asynchronous
    @gen.coroutine
    def post(self):
        name = self.args.get("name", "")
        keyword = self.args.get("keyword", "")
        # keycode = self.args.get("keycode", "")
        response1 = yield gen.Task(
            svc_pt_permission.get_or_create.apply_async,
            args=[name, keyword]
        )
        logger.info(response1.result)
        response = yield gen.Task(
            svc_pt_permission.get_list.apply_async,
            args=[]
        )
        data = {"result": response.result}
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(1).value % PT_Perm.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
        raise gen.Return(self.render("admin/pt_perm/index.html", **data))


@url("/pt_perm/info", name="pt_perm.info", active="pt_perm")
class PT_Perm_Info_Handler(Handler):
    u"""操作权限管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        perm_id = self.args.get("perm_id", 0)
        response = yield gen.Task(svc_pt_permission.get_info.apply_async, args=[perm_id])
        if response.result["return_code"] == 0:
            data = {"result": response.result, "action_name": "pt_perm.info"}
        else:
            data = {"result": response.result, "action_name": "pt_perm"}
        logger.info("data")
        logger.info(data)
        raise gen.Return(self.render("admin/pt_perm/_index_form.html", **data))
