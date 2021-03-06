# -*- coding: utf-8 -*-

from datetime import datetime
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
# from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.models.project import Pro_Event, Pro_Event_Detail
from scloud.const import STATUS_PRO_TABLES
from scloud.models.pt_user import PT_User


class EventService(BaseService):

    @thrownException
    def do_event(self):
        logger.info("------ [do_event] ------")
        try:
            pro_id = int(self.params.get("pro_id"))
        except:
            return self.failure(ERROR.pro_name_empty_err)
        try:            
            res_apply_id = int(self.params.get("res_apply_id"))
        except:
            return self.failure(ERROR.res_apply_id_empty_err)
        title = self.params.get("title")
        content = self.params.get("content")
        priority = int(self.params.get("priority", 0))
        if not pro_id:
            return self.failure(ERROR.pro_name_empty_err)
        if not res_apply_id:
            return self.failure(ERROR.res_apply_id_empty_err)
        if not title:
            return self.failure(ERROR.pro_event_title_empty_err)
        if not content:
            return self.failure(ERROR.pro_event_content_empty_err)
        pro_event, created = Pro_Event.get_or_create_obj(self.db, pro_id=pro_id, res_apply_id=res_apply_id, title=title)
        if created:
            pro_event.pro_id = pro_id
            pro_event.res_apply_id = res_apply_id
            pro_event.priority = priority
            pro_event.title = title
            pro_event.content = content
            pro_event.user_id = self.handler.current_user.id
            self.db.add(pro_event)
            self.db.flush()
        else:
            return self.failure(ERROR.pro_event_title_duplicate_err)
        return self.success(data=pro_event)

    @thrownException
    def get_list(self):
        id = self.params.get("id")
        pro_id = self.params.get("pro_id", 0)
        search = self.params.get("search", "")
        status = self.params.get("status", -3)

        conditions = and_()
        user_id = self.params.get("user_id")
        if user_id:
            pt_user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id
            ).first()
            if pt_user and not pt_user.imchecker:
                conditions.append(Pro_Event.user_id == user_id)
        if id:
            conditions.append(Pro_Event.id == int(id))
        if pro_id:
            conditions.append(Pro_Event.pro_id == int(pro_id))
        if search:
            conditions.append(Pro_Event.title.like('%' + search + '%'))
        if status > -3:
            conditions.append(Pro_Event.status == status)
        pro_users = self.db.query(
            Pro_Event
        ).filter(
            conditions
        ).order_by(Pro_Event.id.desc()).all()
        # logger.info([i.as_dict() for i in pro_users])
        return self.success(data=pro_users)

    @thrownException
    def get_info(self):
        id = self.params.get("id")
        if id:
            pro_event = self.db.query(
                Pro_Event
            ).filter(
                Pro_Event.id == id    
            ).first()
            return self.success(data=pro_event)
        else:
            return self.failure(ERROR.not_found_err)

    @thrownException
    def do_reply(self):
        event_id = self.params.get("id")
        if not event_id:
            return self.failure(ERROR.pro_event_id_empty_err)
        reply_content = self.params.get("reply_content")
        if not reply_content:
            return self.failure(ERROR.pro_event_reply_content_empty_err)
        pro_event = self.db.query(
            Pro_Event
        ).filter(
            Pro_Event.id == event_id
        ).first()
        logger.info(pro_event)
        # logger.info("self.handler.current_user.imchecker: %s" % self.handler.current_user.imchecker)
        if self.handler.current_user.imchecker:
            status = self.params.get("status", 0)
            pro_event.status = status
            pro_event.checker_id = self.handler.current_user.id
            pro_event.check_time = datetime.now()
        else:
            pro_event.status = STATUS_PRO_TABLES.APPLIED
        self.db.add(pro_event)
        event_detail, created = Pro_Event_Detail.get_or_create_obj(self.db, event_id=event_id, content=reply_content)
        event_detail.user_id = self.handler.current_user.id
        self.db.add(event_detail)
        self.db.flush()
        return self.success(data=event_detail)

    @thrownException
    def do_del_pro_event(self):
        id_list = self.params.get("id_list")
        for id in id_list:
            pro_event = self.db.query(
                Pro_Event
            ).filter(
                Pro_Event.id == id    
            ).first()
            self.db.delete(pro_event)
            self.db.flush()
        return self.success(data=None)
