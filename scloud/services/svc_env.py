# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
from scloud.services.svc_pro_resource_apply import mail_title_format
from scloud.services.svc_login import LoginService


class EnvService(BaseService):

    @thrownException
    def get_list(self):
        logger.info("------[get_list]------")
        env_list = self.db.query(
            Env_Info
        ).all()
        return self.success(data=env_list)

    @thrownException
    def add_env(self):
        logger.info("------[add_env]------")
        name = self.params.get("name")
        desc = self.params.get("desc")
        if not name:
            return self.failure(ERROR.env_name_empty_err)
        if not desc:
            return self.failure(ERROR.env_desc_empty_err)
        env = Env_Info()
        env.name = name
        env.desc = desc
        self.db.add(env)
        self.db.flush()
        return self.success(data=env)

    @thrownException
    def get_env(self):
        logger.info("------[add_env]------")
        env_id = self.params.get("env_id")
        env = self.db.query(
            Env_Info
        ).filter(
            Env_Info.id == env_id
        ).first()
        if not env:
            raise NotFoundError()
        return self.success(data=env)

    @thrownException
    def edit_env(self):
        logger.info("------[add_env]------")
        env_id = self.params.get("env_id")
        name = self.params.get("name")
        desc = self.params.get("desc")
        if not name:
            return self.failure(ERROR.env_name_empty_err)
        if not desc:
            return self.failure(ERROR.env_desc_empty_err)
        env = self.db.query(
            Env_Info
        ).filter(
            Env_Info.id == env_id
        ).first()
        if not env:
            raise NotFoundError()
        env.name = name
        env.desc = desc
        self.db.add(env)
        return self.success(data=env)

