# -*- coding: utf-8 -*-

import scloud
from scloud.shortcuts import url
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
from scloud.handlers import Handler, AuthHandler
import requests
import urlparse
import urllib
import urllib2
import simplejson
import time
from tornado.web import asynchronous
from tornado import gen
from scloud.utils.permission import check_perms
from scloud.pubs.pub_tasks import TaskPublish
from scloud.services.svc_profile import ProfileService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError


@url("/user/profile", name="user_profile", active="user_profile")
@url("/user/profile/xget", name="user_profile_xget", active="user_profile")
class ProfileHandler(AuthHandler):
    u'个人设置'
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("XGET",)

    def get_index_page(self, **kwargs):
        svc = ActHistoryService(self, kwargs)
        act_histories_res = svc.get_list()
        # apply_tasks_res = svc.get_res_tasks()
        last_apply_res = svc.get_last_apply()
        if isinstance(act_histories_res, Exception):
            raise act_histories_res
        data = {
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "act_histories_res": act_histories_res,
            # "apply_tasks_res": apply_tasks_res,
            "last_apply_res": last_apply_res,
        }
        pub_svc = TaskPublish(self)
        pub_data = pub_svc.publish_tasks(self.current_user.id, do_publish=False)
        logger.info(pub_data.data)
        data.update(pub_data.data)
        return data

    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/profile/profile/index.html", **data)

    # @check_perms('pro_info.view')
    @unblock
    def xget(self):
        task_svc = TaskPublish(self)
        tasks_res = task_svc.publish_tasks(user_id=self.current_user.id, pro_id=self.args.get("pro_id"), do_publish=False)
        if tasks_res.return_code == 0:
            # tasks = tasks_res.data
            pro_backup_list = tasks_res.data["pro_backup_list"]
            pro_balance_list = tasks_res.data["pro_balance_list"]
            pro_event_list = tasks_res.data["pro_event_list"]
            pro_publish_list = tasks_res.data["pro_publish_list"]
            pro_user_list = tasks_res.data["pro_user_list"]
            task_list = tasks_res.data["task_list"]
            todo_list = pro_backup_list\
                + pro_balance_list\
                + pro_event_list\
                + pro_publish_list\
                + pro_user_list\
                + task_list
            todo_list.sort(key=lambda x: x.update_time)
            todo_list.reverse()
        else:
            todo_list = []
        page = self.getPage(todo_list, numsPerpage=4, page_name='page')
        if self.current_user.imchecker:
            tmpl_todo_list = self.render_to_string("admin/profile/profile/_profile_checker_todo_list.html", page=page)
        else:
            tmpl_todo_list = self.render_to_string("admin/profile/profile/_profile_user_todo_list.html", page=page)
        data = dict(
            tmpl_todo_list=tmpl_todo_list,
        )
        return simplejson.dumps(self.success(data=data))

    @unblock
    def post(self):
        svc = ProfileService(self)
        user_res = svc.set_profile()
        if isinstance(user_res, Exception):
            raise user_res
        tmpl_form = self.render_to_string("admin/profile/profile/_profile_form.html", user_res=user_res, current_user=self.current_user)
        user_profile_res = svc.get_profile()
        if user_res.return_code == 0:
            delattr(self, "_current_user")
            self.session["current_user"] = user_res.data
            self.save_session()

            tmpl = self.render_to_string("admin/profile/profile/_profile_index.html")
            return simplejson.dumps(self.success(data = {
                "tmpl": tmpl,
                "tmpl_form": tmpl_form,
                "user": self.current_user.as_dict()
            }))
        else:
            logger.info(tmpl_form)
            return simplejson.dumps(self.failure(return_code=user_res.return_code, 
                return_message=user_res.return_message,
                data = {
                "tmpl_form": tmpl_form,
                "user": user_profile_res.data.as_dict()
            }))
        # return simplejson.dumps(self.success(data=data))



@url("/task/(?P<task_id>\d+)/confirm_start_date", name="task_confirm", active="user_profile")
class TaskConfirmHandler(ProfileHandler):
    @unblock
    def post(self, **kwargs):
        svc = ActHistoryService(self, kwargs)
        confirm_res = svc.confirm_start_date()
        if isinstance(confirm_res, Exception):
            raise confirm_res
        self.add_message(u"已确认用户信息")
        data = self.get_index_page(**kwargs)
        tmpl = self.render_to_string("admin/profile/profile/index_pjax.html", **data)
        logger.info(tmpl)
        return simplejson.dumps(self.success(data=tmpl))

