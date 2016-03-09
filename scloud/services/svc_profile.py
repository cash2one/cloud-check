# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info, Pro_Resource_Apply
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
from scloud.services.svc_pro_resource_apply import mail_title_format
from scloud.services.svc_login import LoginService


class ProfileService(BaseService):

    @thrownException
    def get_profile(self):
        logger.info("------[get_profile]------")
        current_user = self.handler.current_user
        if current_user:
            # res = project.as_dict()
            # logger.info("project: %s" % res)
            return self.success(data=current_user)
        else:
            return NotFoundError()

    @thrownException
    def set_profile(self):
        logger.info("------[set_profile]------")
        user_id = int(self.params.get("user_id"))
        username = self.params.get("username")
        email = self.params.get("email")
        mobile = self.params.get("mobile")
        current_user = self.handler.current_user
        if current_user:
            if current_user.id != user_id:
                raise NotFoundError()
            user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id
            ).first()
            user.username = username
            user.email = email
            user.mobile = mobile
            self.db.add(user)
            logger.info("*"*60)
            logger.info(user.username)
            logger.info("*"*60)
            login = LoginService(self.handler)
            login.set_user_attrs(user)
            
            # res = project.as_dict()
            # logger.info("project: %s" % res)
            return self.success(data=user)
        else:
            return NotFoundError()
