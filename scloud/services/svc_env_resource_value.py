# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Resource_Value
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
from scloud.services.svc_pro_resource_apply import ProResourceApplyService



class EnvResourceValueService(ProResourceApplyService):

    # @thrownException
    # def get_list(self):
    #     logger.info("------[get_list]------")
    #     env_list = self.db.query(
    #         Env_Info
    #     ).all()
    #     return self.success(data=env_list)

    # @thrownException
    # def add_env(self):
    #     logger.info("------[add_env]------")
    #     name = self.params.get("name")
    #     desc = self.params.get("desc")
    #     if not name:
    #         return self.failure(ERROR.env_name_empty_err)
    #     if not desc:
    #         return self.failure(ERROR.env_desc_empty_err)
    #     env = Env_Info()
    #     env.name = name
    #     env.desc = desc
    #     self.db.add(env)
    #     self.db.flush()
    #     return self.success(data=env)

    # @thrownException
    # def get_env(self):
    #     logger.info("------[add_env]------")
    #     env_id = self.params.get("env_id")
    #     env = self.db.query(
    #         Env_Info
    #     ).filter(
    #         Env_Info.id == env_id
    #     ).first()
    #     if not env:
    #         raise NotFoundError()
    #     return self.success(data=env)
    @thrownException
    def get_env_resource_value(self):
        env_id = self.params.get("env_id")
        env = self.db.query(
            Env_Resource_Value
        ).filter(
            Env_Resource_Value.env_id == env_id
        ).first()
        return self.success(data=env)

    @thrownException
    def get_or_create(self):
        logger.info("------[get_or_create]------")
        form_valid_res = self.check_form_valid()
        if form_valid_res.return_code < 0:
            return form_valid_res
        env_id = self.params.get("env_id")
        computer = self.params.get("computer")
        cpu = self.params.get("cpu")
        memory = self.params.get("memory")
        disk = self.params.get("disk")
        disk_backup = self.params.get("disk_backup")
        out_ip = self.params.get("out_ip")
        snapshot = self.params.get("snapshot")
        loadbalance = self.params.get("loadbalance")
        internet_ip = self.params.get("internet_ip")
        internet_ip_ssl = self.params.get("internet_ip_ssl")
        env, created = Env_Resource_Value.get_or_create_obj(db=self.db, env_id=env_id)
        logger.info("&"*60)
        logger.info(env)
        env.computer = computer
        env.cpu = cpu
        env.memory = memory
        env.disk = disk
        env.disk_backup = disk_backup
        env.out_ip = out_ip
        env.snapshot = snapshot
        env.loadbalance = loadbalance
        env.internet_ip = internet_ip
        env.internet_ip_ssl = internet_ip_ssl
        self.db.add(env)
        self.db.flush()
        return self.success(data=env)

