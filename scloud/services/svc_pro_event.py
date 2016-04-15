# -*- coding: utf-8 -*-

# from tornado import gen
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
# from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.models.project import Pro_Event


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
        pro_user, created = Pro_Event.get_or_create_obj(self.db, pro_id=pro_id, res_apply_id=res_apply_id, title=title)
        if created:
            pro_user.pro_id = pro_id
            pro_user.res_apply_id = res_apply_id
            pro_user.priority = priority
            pro_user.title = title
            pro_user.content = content
            pro_user.user_id = self.handler.current_user.id
            self.db.add(pro_user)
            self.db.flush()
        else:
            return self.failure(ERROR.pro_event_title_duplicate_err)
        return self.success(data=pro_user)

    @thrownException
    def get_list(self):
        pro_id = int(self.params.get("pro_id", 0))
        conditions = and_()
        if pro_id:
            conditions.append(Pro_Event.pro_id == pro_id)
        pro_users = self.db.query(
            Pro_Event
        ).filter(
            conditions
        ).all()
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
    def do_del_pro_user(self):
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
