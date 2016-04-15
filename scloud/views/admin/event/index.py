#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import simplejson
from scloud.shortcuts import url
from scloud.config import logger
from scloud.const import STATUS_PRO_TABLES
from scloud.handlers import AuthHandler
from scloud.utils.permission import check_perms
from scloud.services.svc_project import ProjectService
from scloud.services.svc_pro_event import EventService
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError


class GuideStepGetHandler(AuthHandler):
    def get_pro_info_res(self, pro_id):
        kw = {"pro_id": pro_id}
        svc = ProjectService(self, kw)
        pro_info_res = svc.get_project()
        if isinstance(pro_info_res, Exception):
            raise pro_info_res
        data = {
            "pro_info_res": pro_info_res,
            "STATUS_RESOURCE": STATUS_RESOURCE,
        }
        return data


@url("/event/index", name="event.index", active="event.index")
class EventIndexHandler(GuideStepGetHandler):
    u'事件列表'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = {
            "pro_list_res": pro_list_res,
        }
        return self.render_to_string("admin/event/index.html", **data)


@url("/event/add", name="event.add", active="event.index")
class EventAddHandler(GuideStepGetHandler):
    u'创建事件'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = dict(pro_list_res=pro_list_res)
        return self.render_to_string("admin/event/add.html", **data)

    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = EventService(self)
        do_event_res = svc.do_event()
        if do_event_res.return_code < 0:
            self.add_message(u"事件提交失败 %s(%s)" % (do_event_res.return_code, do_event_res.return_message), level="warning")
        else:
            self.add_message(u"事件提交成功", level="success")

        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = dict(pro_list_res=pro_list_res, do_event_res=do_event_res)
        tmpl = self.render_to_string("admin/event/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
