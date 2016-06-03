# -*- coding: utf-8 -*-

import scloud
import simplejson
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger
from scloud.utils.permission import check_perms
from scloud.services.svc_project import ProjectService
from scloud.utils.unblock import unblock
from scloud.pubs.pub_tasks import TaskPublish
from .base import ApplyHandler
from scloud.handlers import AuthHandler
from tornado.util import ObjectDict
from scloud.const import STATUS_RESOURCE
from scloud.services.svc_pro_event import EventService


@url("/apply/project/detail", name="apply.project.detail", active="apply.project")
class PublishDetailHandler(ApplyHandler):
    u'项目详情'
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("XGET",)

    @property
    def bread_list(self):
        _bread_list = [
            {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"}
        ]
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        project_res = svc.get_project()
        logger.info("[project_res]: %s" % project_res)
        data = {
            "project_res": project_res,
        }
        return self.render_to_string("admin/apply/project/detail.html", **data)

    @check_perms('pro_info.view')
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
        page = self.getPage(todo_list, page_name='todo_page')
        tmpl_todo_list = self.render_to_string("admin/apply/project/_pro_todo_list.html", page=page)

        svc = ProjectService(self)
        project_res = svc.get_project()
        if project_res.return_code == 0:
            pro_info = project_res.data
            last_apply = pro_info.last_apply
            if last_apply:
                pro_resource_apply_res = ObjectDict()
                pro_resource_apply_res.return_code = 0
                pro_resource_apply_res.return_message = u""
                pro_resource_apply_res.data = last_apply
                tmpl_pro_resource_apply_detail = self.render_to_string("admin/apply/project/_pro_resource_apply_detail.html", pro_resource_apply_res=pro_resource_apply_res)
            else:
                pro_resource_apply_res = ObjectDict()
                pro_resource_apply_res.return_code = STATUS_RESOURCE.UNKNOWN
                pro_resource_apply_res.return_message = STATUS_RESOURCE.unknown.value
                tmpl_pro_resource_apply_detail = self.render_to_string("admin/apply/project/_pro_resource_apply_detail.html", pro_resource_apply_res=pro_resource_apply_res)

        else:
            tmpl_pro_resource_apply_detail = self.render_to_string("admin/apply/project/_pro_resource_apply_detail.html", pro_resource_apply_res=project_res)

        evt_svc = EventService(self)
        pro_events_res = evt_svc.get_list()
        logger.info(pro_events_res)
        tmpl_pro_events = self.render_to_string("admin/apply/project/_pro_events.html", pro_events_res=pro_events_res, project_res=project_res)

        data = dict(
            tmpl_todo_list=tmpl_todo_list,
            tmpl_pro_resource_apply_detail=tmpl_pro_resource_apply_detail,
            tmpl_pro_events=tmpl_pro_events,
        )
        return simplejson.dumps(self.success(data=data))
