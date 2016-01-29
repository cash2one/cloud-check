#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from torweb.urls import url
from scloud.const import act_actions
from scloud.config import logger
from scloud.handlers import Handler, AuthHandler
from scloud.models.pt_user import PT_User, PT_User_Role
from tornado.web import asynchronous
from tornado import gen
from scloud.async_services import svc_pt_user
from pprint import pprint
from scloud.utils import green
from scloud.utils.permission import check_perms


@url("/pt_user", name="pt_user", active="pt_user")
class PT_User_Handler(AuthHandler):
    u"""用户管理"""
    @check_perms("pro_info.view")
    @gen.coroutine
    def genReturn(self):
        search = self.args.get("search", "")
        response = yield gen.Task(svc_pt_user.get_list.apply_async, args=[search])
        data = {"result": response.result}
        pprint(data)
        raise gen.Return(self.render("admin/pt_user/index.html", **data))

    @asynchronous
    @gen.coroutine
    def get(self):
        yield gen.Task(self.genReturn)

    @asynchronous
    @gen.coroutine
    def post(self):
        method = self.args.get("_method", "")
        if method == "DELETE":
            yield gen.Task(self.delete_user)
        else:
            yield gen.Task(self.post_user)

    @gen.coroutine
    def delete_user(self):
        user_id = self.args.get("user_id", 0)
        response1 = yield gen.Task(svc_pt_user.delete_info.apply_async, args=[user_id])
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(3).value % PT_User.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
        yield gen.Task(self.genReturn)

    @asynchronous
    @gen.coroutine
    def post_user(self):
        username = self.args.get("username", "")
        password = self.args.get("password", "")
        response1 = yield gen.Task(
            svc_pt_user.get_or_create.apply_async,
            args=[username, password]
        )
        logger.info(response1.result)
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(1).value % PT_User.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
        yield gen.Task(self.genReturn)


@url("/pt_user/info", name="pt_user.info", active="pt_user")
class PT_User_Info_Handler(Handler):
    u"""用户管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.args.get("user_id", 0)
        response = yield gen.Task(svc_pt_user.get_info.apply_async, args=[user_id])
        if response.result["return_code"] == 0:
            data = {"result": response.result, "action_name": "pt_user.info"}
        else:
            data = {"result": response.result, "action_name": "pt_user"}
        logger.info("data")
        pprint(data)
        raise gen.Return(self.render("admin/pt_user/_index_form.html", **data))

    @gen.coroutine
    def post(self):
        user_id = self.args.get("user_id", 0)
        username = self.args.get("username", u"")
        password = self.args.get("password", u"")
        response1 = yield gen.Task(svc_pt_user.update_info.apply_async, args=[user_id, username, password])
        if response1.result["return_code"] == 0:
            self.add_message(u"%s成功!" % act_actions.get(2).value % PT_User.__doc__, level="success")
            data = {"result": {"return_code": 0, "return_message": u"", "data": self.args}}
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
            data = {"result": response1.result}
        response = yield gen.Task(
            svc_pt_user.get_list.apply_async,
            args=[]
        )
        data = {"result": response.result, "action_name": "pt_user.info"}
        raise gen.Return(self.render("admin/pt_user/index.html", **data))


@url("/pt_user/roles/info", name="pt_user.role_info", active="pt_user")
class PT_User_Role_Info_Handler(Handler):
    u"""用户管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.args.get("user_id", 0)
        response = yield gen.Task(svc_pt_user.get_user_roles.apply_async, args=[user_id])
        data = {"user_id": user_id, "action_name": "pt_user.role_info"}
        if response.result["return_code"] == 0:
            data.update({"result": response.result})
        logger.info("data")
        logger.info(data)
        raise gen.Return(self.render("admin/pt_user/_index_user_roles_form.html", **data))

    @asynchronous
    @gen.coroutine
    def post(self):
        user_id = self.args.get("user_id", 0)
        role_ids = self.get_arguments("role_id")
        # group_op_list = [(g, op) for g, op in [_str.split(".") for _str in group_ops]]
        logger.info(role_ids)
        response1 = yield gen.Task(svc_pt_user.post_user_roles.apply_async, args=[user_id, role_ids])
        response = yield gen.Task(
            svc_pt_user.get_list.apply_async,
            args=[]
        )
        data = {"result": response.result}
        if response1.result["return_code"] == 0:
            data.update(response1.result["data"])
        logger.info("data")
        logger.info(data)
        self.add_message(u"%s成功!" % act_actions.get(2).value % PT_User_Role.__doc__, level="success")
        # data = {}
        raise gen.Return(self.render("admin/pt_user/index.html", **data))


@url("/pt_user/delete", name="pt_user.delete", active="pt_user")
class PT_User_Delete_Handler(Handler):
    u"""用户管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.args.get("user_id", 0)
        data = {"user_id": user_id, "action_name": "pt_user.role_info"}
        raise gen.Return(self.render("admin/pt_user/_index_user_delete_form.html", **data))
