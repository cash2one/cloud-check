#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import simplejson
from scloud.shortcuts import url
from scloud.config import logger
# from scloud.const import STATUS_PRO_TABLES
from scloud.handlers import AuthHandler
from scloud.utils.permission import check_perms
from scloud.services.svc_project import ProjectService
from scloud.services.svc_pro_event import EventService
from scloud.async_services.publish_task import publish_notice_checker, publish_notice_user
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
            # "STATUS_RESOURCE": STATUS_RESOURCE,
        }
        return data


@url("/apply/event/index", name="apply.event", active="event.index")
@url("/event/index", name="event.index", active="event.index")
class EventIndexHandler(GuideStepGetHandler):
    u'事件列表'

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
            ]
        else:
            _bread_list = []
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = EventService(self, {"user_id": self.current_user.id})
        pro_events_res = svc.get_list()
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = {
            "pro_list_res": pro_list_res,
            "pro_events_res": pro_events_res,
            "page": self.getPage(pro_events_res.data)
        }
        return self.render_to_string("admin/event/index.html", **data)


@url("/event/detail", name="event.detail", active="event.index")
class EventDetailHandler(GuideStepGetHandler):
    u'事件详情'
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
                {"urlspec": url.handlers_dict.get('apply.event'), "url": self.session.get("from_url"), "icon": "files-o"},
            ]
        else:
            _bread_list = [
                {"urlspec": url.handlers_dict.get('apply.event'), "url": self.session.get("from_url"), "icon": "files-o"},
            ]
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = EventService(self)
        pro_event_res = svc.get_info()
        if pro_event_res.return_code < 0:
            raise SystemError(pro_event_res.return_code, pro_event_res.return_message)
        logger.info(pro_event_res)
        data = {
            "pro_event_res": pro_event_res,
        }
        return self.render_to_string("admin/event/detail.html", **data)

    @check_perms('pro_info.view')
    @unblock
    def post(self):
        return self.reply(template="admin/event/detail_pjax.html")

    @check_perms('pro_info.check')
    @unblock
    def check(self):
        return self.reply(template="admin/check/_event_pro_event_detail.html")

    def reply(self, template=""):
        svc = EventService(self)
        pro_event_res = svc.do_reply()
        logger.info(pro_event_res)
        # if pro_event_detail_res.return_code < 0:
        #     self.add_message(u"回复事件失败！(%s)%s" % (pro_event_detail_res.return_code, pro_event_detail_res.return_message), level="warning")
        # else:
        #     self.add_message(u"回复事件成功！", level="success")
        pro_event_res = svc.get_info()
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        logger.info(pro_event_res)
        data = {
            "pro_event_res": pro_event_res,
            "pro_list_res": pro_list_res,
        }
        if self.current_user.imchecker:
            publish_notice_user.delay(pro_event_res.data.user.id)
        else:
            publish_notice_checker.delay(self.current_user.id)
        tmpl = self.render_to_string(template, **data)
        return simplejson.dumps(self.success(data=tmpl))


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
            template = "admin/event/add_pjax.html"
        else:
            self.add_message(u"事件提交成功", level="success")
            template = "admin/event/detail_pjax.html"

        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = dict(pro_list_res=pro_list_res, pro_event_res=do_event_res)
        tmpl = self.render_to_string(template, **data)
        return simplejson.dumps(self.success(data=tmpl))


@url("/apply/event/del", name="apply.event.del", active="apply.event")
class EventDelHandler(GuideStepGetHandler):
    u'删除事件'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        id_list = self.get_arguments("id")
        svc = EventService(self, {"id_list": id_list})
        del_res = svc.do_del_pro_event()
        logger.info(del_res)
        if del_res.return_code == 0:
            self.add_message(u"事件信息删除成功！", level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"事件信息删除失败！(%s)(%s)" % (del_res.return_code, del_res.return_message), level="warning")
        svc = EventService(self, {"user_id": self.current_user.id})
        pro_events_res = svc.get_list()
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data = {
            "pro_list_res": pro_list_res,
            "pro_events_res": pro_events_res,
            "page": self.getPage(pro_events_res.data)
        }
        tmpl = self.render_to_string("admin/event/index_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
