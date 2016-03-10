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
from scloud.models.base import db_engine


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
        logger.info("------[get_env]------")
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
        logger.info("------[edit_env]------")
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

    @thrownException
    def del_env_info(self):
        logger.info("------[del_env_info]------")
        env_ids = self.params.get("env_ids")
        or_conditions = or_()
        for env_id in env_ids:
            # or_conditions.append(Env_Info.id == env_id)
            or_conditions.append(Env_Info.__table__.c.id == env_id)
        env_info_query_list = self.db.query(
            Env_Info
        ).filter(
            or_conditions
        )
        messages = []
        logger.info("-------------query------------------")
        for env in env_info_query_list.all():
            messages.append(u"环境[%s(%s)]已经删除成功！" % (env.name, env.id))
            self.db.delete(env)
            logger.info("--------------[session delete]-----------------")
        # env_info_query_list = self.db.query(
        #     Env_Info
        # ).filter(
        #     or_conditions
        # ).delete()
        self.db.flush()
        logger.info("--------------[flush]-----------------")
        # env_info_query_list.delete()
        # conn = db_engine.connect()
        # conn.execute(
        #     Env_Info.__table__.delete().where(
        #         or_conditions
        #         # Env_Info.__table__.c.id == 
        #     )
        # )
        # self.db.delete(env_info_query_list)
        return self.success(data=messages)

