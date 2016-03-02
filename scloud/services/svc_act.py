# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.act import Act_History
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types


class ActHistoryService(BaseService):

    @thrownException
    def get_list(self):
        logger.info("------[get_profile]------")
        current_user = self.handler.current_user
        if current_user:
            history_list = self.db.query(
                Act_History
            ).filter(
                Act_History.user_id == current_user.id
            ).order_by(
                Act_History.id.desc()
            ).limit(10)

            # res = project.as_dict()
            # logger.info("project: %s" % res)
            return self.success(data=history_list)
        else:
            return NotFoundError()

