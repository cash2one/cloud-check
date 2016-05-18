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
from voluptuous import Schema, ALLOW_EXTRA


class EnvResourceValueService(ProResourceApplyService):

    def get_param_schema(self):
        param_schema = Schema({
            "computer": self.validate_num_more_than_1,
            "cpu": self.validate_num_more_than_1,
            "memory": self.validate_num_more_than_1,
            'disk': self.validate_num,
            'disk_amount': self.validate_num,
            'disk_backup': self.validate_num,
            'disk_backup_amount': self.validate_num,
            'out_ip': self.validate_num,
            'snapshot': self.validate_num,
            'loadbalance': self.validate_num,
            'internet_ip': self.validate_num,
            # 'bandwidth': self.validate_num,
            'internet_ip_ssl': self.validate_num,
            'period': self.validate_num_more_than_1,
        }, extra=ALLOW_EXTRA)
        return param_schema

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
        param_schema = self.get_param_schema()
        form_valid_res = self.check_form_valid(param_schema)
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

