# -*- coding: utf-8 -*-

import scloud
import simplejson
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger
from scloud.utils.permission import check_perms
from scloud.services.svc_project import ProjectService
from scloud.services.svc_env import EnvService
from scloud.utils.unblock import unblock
# from scloud.pubs.pub_tasks import TaskPublish
from scloud.handlers import AuthHandler


@url("/project/list", name="project.list", active="project.list")
@url("/project/list/xget", name="project.list.xget", active="project.list")
class PublishDetailHandler(AuthHandler):
    u'项目列表'
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("XGET",)

    @check_perms('pro_info.view, pro_info.check', _and=False)
    @unblock
    def get(self):
        svc = EnvService(self)
        env_list_res = svc.get_list()
        data = dict(
            env_list_res = env_list_res,
        )
        return self.render_to_string("admin/project/list.html", **data)

    @unblock
    def xget(self):
        svc = ProjectService(self)
        project_list_res = svc.filter_list()
        if project_list_res.return_code == 0:
            project_list = project_list_res.data.projects
            projects_by_env = project_list_res.data.projects_by_env
            projects_by_status = project_list_res.data.projects_by_status
        else:
            project_list = []
        page = self.getPage(project_list)
        data = dict(
            page = page,
            projects_by_env = projects_by_env,
            projects_by_status = projects_by_status
        )
        tmpl_project_list = self.render_to_string("admin/project/_project_list.html", **data)
        # tmpl_project_charts = self.render_to_string("admin/project/_project_charts.html", **data)
        tmpl_project_charts = self.render_to_string("admin/project/_project_chartjs_charts.html", **data)
        return simplejson.dumps(self.success(data=dict(
            tmpl_project_list=tmpl_project_list,
            tmpl_project_charts=tmpl_project_charts,
        )))
