#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from torweb.urls import url
from scloud.const import act_actions
from scloud.config import logger
from scloud.handlers import Handler
from scloud.models.pt_user import PT_Role
from tornado.web import asynchronous
from tornado import gen
from scloud.async_services import svc_pt_role


@url("/pt_role", name="pt_role", active="pt_role")
class PT_Role_Handler(Handler):
    u"""角色组管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        search = self.args.get("search", "")
        response = yield gen.Task(svc_pt_role.get_list.apply_async, args=[search])
        data = {"result": response.result}
        raise gen.Return(self.render("admin/pt_role/index.html", **data))

    @asynchronous
    @gen.coroutine
    def post(self):
        name = self.args.get("name", "")
        desc = self.args.get("desc", "")
        remark = self.args.get("remark", "")
        response1 = yield gen.Task(
            svc_pt_role.get_or_create.apply_async,
            args=[name, desc, remark]
        )
        logger.info(response1.result)
        response = yield gen.Task(
            svc_pt_role.get_list.apply_async,
            args=[]
        )
        data = {"result": response.result}
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(1).value % PT_Role.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
        raise gen.Return(self.render("admin/pt_role/index.html", **data))


@url("/pt_role/info", name="pt_role.info", active="pt_role")
class PT_Role_Info_Handler(Handler):
    u"""角色组管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        role_id = self.args.get("role_id", 0)
        response = yield gen.Task(svc_pt_role.get_info.apply_async, args=[role_id])
        if response.result["return_code"] == 0:
            data = {"result": response.result, "action_name": "pt_role.info"}
        else:
            data = {"result": response.result, "action_name": "pt_role"}
        logger.info("data")
        logger.info(data)
        raise gen.Return(self.render("admin/pt_role/_index_form.html", **data))

    @asynchronous
    @gen.coroutine
    def post(self):
        role_id = self.args.get("role_id", 0)
        name = self.args.get("name", u"")
        desc = self.args.get("desc", u"")
        remark = self.args.get("remark", u"")
        response1 = yield gen.Task(svc_pt_role.update_info.apply_async, args=[role_id, name, desc, remark])
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(2).value % PT_Role.__doc__, level="success")
            data = {"result": {"return_code": 0, "return_message": u"", "data": self.args}}
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
            data = {"result": response1.result}
        response = yield gen.Task(
            svc_pt_role.get_list.apply_async,
            args=[]
        )
        data = {"result": response.result}
        raise gen.Return(self.render("admin/pt_role/index.html", **data))


@url("/pt_role/groups/info", name="pt_role.group_info", active="pt_role")
class PT_Role_Group_Info_Handler(Handler):
    u"""角色组管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        # role_id = self.args.get("role_id", 0)
        # response = yield gen.Task(svc_pt_role.get_group_ops.apply_async, args=[role_id])
        # if response.result["return_code"] == 0:
        #     data = {"result": response.result, "action_name": "pt_role.info"}
        # else:
        #     data = {"result": response.result, "action_name": "pt_role"}
        # logger.info("data")
        # logger.info(data)
        data = {}
        raise gen.Return(self.render("admin/pt_role/_index_group_ops_form.html", **data))
