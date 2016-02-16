#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from torweb.urls import url
from scloud.const import act_actions
from scloud.config import logger
from scloud.handlers import Handler, AuthHandler
from scloud.models.pt_user import PT_Role, PT_Role_Group_Ops
from tornado.web import asynchronous
from tornado import gen
from scloud.async_services import svc_pt_role
from pprint import pprint


@url("/pt_role", name="pt_role", active="pt_role")
class PT_Role_Handler(AuthHandler):
    u"""角色组管理"""
    @gen.coroutine
    def genReturn(self):
        search = self.args.get("search", "")
        response = yield gen.Task(svc_pt_role.get_list.apply_async, args=[search])
        data = {"result": response.result}
        pprint(data)
        raise gen.Return(self.render("admin/pt_role/index.html", **data))

    @asynchronous
    @gen.coroutine
    def get(self):
        yield gen.Task(self.genReturn)

    @asynchronous
    @gen.coroutine
    def post(self):
        method = self.args.get("_method", "")
        if method == "DELETE":
            yield gen.Task(self.delete_role)
        else:
            yield gen.Task(self.post_role)

    @gen.coroutine
    def delete_role(self):
        role_id = self.args.get("role_id", 0)
        response1 = yield gen.Task(svc_pt_role.delete_info.apply_async, args=[role_id])
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(3).value % PT_Role.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
        yield gen.Task(self.genReturn)

    @asynchronous
    @gen.coroutine
    def post_role(self):
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
class PT_Role_Info_Handler(AuthHandler):
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
        pprint(data)
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
        data = {"result": response.result, "action_name": "pt_role.info"}
        raise gen.Return(self.render("admin/pt_role/index.html", **data))


@url("/pt_role/groups/info", name="pt_role.group_info", active="pt_role")
class PT_Role_Group_Info_Handler(AuthHandler):
    u"""角色组管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        role_id = self.args.get("role_id", 0)
        response = yield gen.Task(svc_pt_role.get_role_group_ops.apply_async, args=[role_id])
        data = {"role_id": role_id, "action_name": "pt_role.group_info"}
        if response.result["return_code"] == 0:
            data.update({"result": response.result})
        logger.info("data")
        logger.info(data)
        raise gen.Return(self.render("admin/pt_role/_index_group_ops_form.html", **data))

    @asynchronous
    @gen.coroutine
    def post(self):
        role_id = self.args.get("role_id", 0)
        group_ops = self.get_arguments("group_op")
        # group_op_list = [(g, op) for g, op in [_str.split(".") for _str in group_ops]]
        logger.info(group_ops)
        response1 = yield gen.Task(svc_pt_role.post_role_group_ops.apply_async, args=[role_id, group_ops])
        response = yield gen.Task(
            svc_pt_role.get_list.apply_async,
            args=[]
        )
        data = {"result": response.result}
        if response1.result["return_code"] == 0:
            data.update(response1.result["data"])
        logger.info("data")
        logger.info(data)
        self.add_message(u"%s成功!" % act_actions.get(2).value % PT_Role_Group_Ops.__doc__, level="success")
        # data = {}
        raise gen.Return(self.render("admin/pt_role/index.html", **data))


@url("/pt_role/delete", name="pt_role.delete", active="pt_role")
class PT_role_Delete_Handler(AuthHandler):
    u"""用户管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        role_id = self.args.get("role_id", 0)
        data = {"role_id": role_id}
        raise gen.Return(self.render("admin/pt_role/_index_role_delete_form.html", **data))
