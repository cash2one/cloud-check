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
from scloud.services.svc_pt_user import PtUserService
from pprint import pprint
from scloud.utils.unblock import unblock
from scloud.utils.permission import check_perms


@url("/pt_user", name="pt_user", active="pt_user")
class PT_User_Handler(AuthHandler):
    u"""用户管理"""
    def get_index_page(self):
        svc = PtUserService(self)
        response = svc.get_list()
        # search = self.args.get("search", "")
        # response = yield gen.Task(svc_pt_user.get_list.apply_async, args=[search])
        data = {"result": response}
        pprint(data)
        return self.render_to_string("admin/pt_user/index.html", **data)

    @unblock
    def get(self):
        return self.get_index_page()

    @unblock
    def post(self):
        method = self.args.get("_method", "")
        if method == "DELETE":
            return self.delete_user()
        else:
            return self.post_user()

    def delete_user(self):
        svc = PtUserService(self)
        response1 = svc.delete_info()
        # user_id = self.args.get("user_id", 0)
        # response1 = yield gen.Task(svc_pt_user.delete_info.apply_async, args=[user_id])
        if response1.return_code == 0:
            self.add_message(u"%s成功!" % act_actions.get(3).value % PT_User.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.return_code, response1.return_message), level="warning")
        return self.get_index_page()

    def post_user(self):
        svc = PtUserService(self)
        response1 = svc.get_or_create()
        # username = self.args.get("username", "")
        # password = self.args.get("password", "")
        # response1 = yield gen.Task(
        #     svc_pt_user.get_or_create.apply_async,
        #     args=[username, password]
        # )
        # logger.info(response1.result)
        if response1.return_code == 0:
            self.add_message(u"%s成功!" % act_actions.get(1).value % PT_User.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.return_code, response1.return_message), level="warning")
        return self.get_index_page()


@url("/pt_user/info", name="pt_user.info", active="pt_user")
class PT_User_Info_Handler(Handler):
    u"""用户管理"""
    @unblock
    def get(self):
        svc = PtUserService(self)
        response = svc.get_info()
        # user_id = self.args.get("user_id", 0)
        # response = yield gen.Task(svc_pt_user.get_info.apply_async, args=[user_id])
        if isinstance(response, Exception):
            data = {"result": response, "action_name": "pt_user"}
        else:
            data = {"result": response, "action_name": "pt_user.info"}
        return self.render_to_string("admin/pt_user/_index_form.html", **data)

    @unblock
    def post(self):
        svc = PtUserService(self)
        response1 = svc.update_info()
        if response1.return_code == 0:
            self.add_message(u"%s成功!" % act_actions.get(2).value % PT_User.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.return_code, response1.return_message), level="warning")
        response = svc.get_list()
        data = {"result": response, "action_name": "pt_user.info"}
        raise gen.Return(self.render("admin/pt_user/index.html", **data))


@url("/pt_user/roles/info", name="pt_user.role_info", active="pt_user")
class PT_User_Role_Info_Handler(Handler):
    u"""用户管理"""
    @unblock
    def get(self):
        svc = PtUserService(self)
        response = svc.get_user_roles()
        user_id = self.args.get("user_id", 0)
        logger.info(response)
        data = {"user_id": user_id, "action_name": "pt_user.role_info"}
        if response.return_code == 0:
            data.update({"result": response})
        response = svc_pt_user.get_user_roles(user_id)
        return self.render_to_string("admin/pt_user/_index_user_roles_form.html", **data)

    @unblock
    def post(self):
        role_ids = self.get_arguments("role_id")
        svc = PtUserService(self, {"role_ids": role_ids})
        response1 = svc.post_user_roles()
        response = svc.get_list()
        # user_id = self.args.get("user_id", 0)
        # group_op_list = [(g, op) for g, op in [_str.split(".") for _str in group_ops]]
        # logger.info(role_ids)
        # response1 = yield gen.Task(svc_pt_user.post_user_roles.apply_async, args=[user_id, role_ids])
        # response = yield gen.Task(
        #     svc_pt_user.get_list.apply_async,
        #     args=[]
        # )
        data = {"result": response}
        if response1.return_code == 0:
            data.update(response1.data)
        logger.info("data")
        logger.info(data)
        self.add_message(u"%s成功!" % act_actions.get(2).value % PT_User_Role.__doc__, level="success")
        # data = {}
        return self.render_to_string("admin/pt_user/index.html", **data)


@url("/pt_user/delete", name="pt_user.delete", active="pt_user")
class PT_User_Delete_Handler(Handler):
    u"""用户管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.args.get("user_id", 0)
        data = {"user_id": user_id, "action_name": "pt_user.role_info"}
        raise gen.Return(self.render("admin/pt_user/_index_user_delete_form.html", **data))
