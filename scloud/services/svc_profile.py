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

