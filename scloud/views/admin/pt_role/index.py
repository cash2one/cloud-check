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
from scloud.utils.unblock import unblock
from scloud.async_services import svc_pt_role
from scloud.services.svc_pt_role import PtRoleService
from pprint import pprint


@url("/pt_role", name="pt_role", active="pt_role")
class PT_Role_Handler(AuthHandler):
    u"""角色组管理"""
    @unblock
    def get(self):
        return self.get_index_page()

    def get_index_page(self):
        svc = PtRoleService(self)
        result = svc.get_list()
        data = {"result": result}
        return self.render_to_string("admin/pt_role/index.html", **data)

    @unblock
    def post(self):
        method = self.args.get("_method", "")
        if method == "DELETE":
            return self.delete_role()
        else:
            return self.post_role()

    def delete_role(self):
        svc = PtRoleService(self)
        del_res = svc.delete_info()
        if del_res.return_code == 0:
            self.add_message(u"%s成功!" % act_actions.get(3).value % PT_Role.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.result["return_code"], response1.result["return_message"]), level="warning")
        return self.get_index_page()

    def post_role(self):
        svc = PtRoleService(self)
        response1 = svc.get_or_create()
        if response1.return_code == 0:
            self.add_message(u"%s成功!" % act_actions.get(1).value % PT_Role.__doc__, level="success")
        else:
            self.add_message(u"failure code (%s): %s" % (response1.return_code, response1.return_message), level="warning")
        return self.get_index_page()


@url("/pt_role/info", name="pt_role.info", active="pt_role")
class PT_Role_Info_Handler(AuthHandler):
    u"""角色组管理"""
    @unblock
    def get(self):
        svc = PtRoleService(self)
        response = svc.get_info()
        # logger.info(response)
        if isinstance(response, Exception):
            data = {"result": response, "action_name": "pt_role"}
        else:
            data = {"result": response, "action_name": "pt_role.info"}
        return self.render_to_string("admin/pt_role/_index_form.html", **data)

    @unblock
    def post(self):
        svc = PtRoleService(self)
        response1 = svc.update_info()
        if response1.return_code == 0:
            self.add_message(u"%s成功!" % act_actions.get(2).value % PT_Role.__doc__, level="success")
            data = {"result": {"return_code": 0, "return_message": u"", "data": self.args}}
        else:
            self.add_message(u"failure code (%s): %s" % (response1.return_code, response1.return_message), level="warning")
            data = {"result": response1}

        response = svc.get_list()
        data = {"result": response, "action_name": "pt_role.info"}
        return self.render_to_string("admin/pt_role/index.html", **data)


@url("/pt_role/groups/info", name="pt_role.group_info", active="pt_role")
class PT_Role_Group_Info_Handler(AuthHandler):
    u"""角色组管理"""
    @unblock
    def get(self):
        svc = PtRoleService(self)
        response = svc.get_role_group_ops()
        role_id = self.args.get("role_id", 0)
        #@ response = yield gen.Task(svc_pt_role.get_role_group_ops.apply_async, args=[role_id])
        data = {"role_id": role_id, "action_name": "pt_role.group_info"}
        if response.return_code == 0:
            data.update({"result": response})
        return self.render_to_string("admin/pt_role/_index_group_ops_form.html", **data)

    @unblock
    def post(self):
        group_ops = self.get_arguments("group_op")
        svc = PtRoleService(self, {"group_ops": group_ops})
        response1 = svc.post_role_group_ops()
        logger.info(group_ops)
        response = svc.get_list()
        data = {"result": response}
        if response1.return_code == 0:
            data.update(response1.data)
        self.add_message(u"%s成功!" % act_actions.get(2).value % PT_Role_Group_Ops.__doc__, level="success")
        return self.render_to_string("admin/pt_role/index.html", **data)


@url("/pt_role/delete", name="pt_role.delete", active="pt_role")
class PT_role_Delete_Handler(AuthHandler):
    u"""用户管理"""
    @asynchronous
    @gen.coroutine
    def get(self):
        role_id = self.args.get("role_id", 0)
        data = {"role_id": role_id}
        raise gen.Return(self.render("admin/pt_role/_index_role_delete_form.html", **data))
