# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Resource_Fee
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from voluptuous import (Schema, Required, Error,
    Invalid, ALLOW_EXTRA, MultipleInvalid, TypeInvalid, ValueInvalid,
    All, Length, Range)


class EnvResourceFeeService(ProResourceApplyService):
    def validate_float(self, value):
        if str(value).strip() == '':
            value = 0
        if not isinstance(value, float):
            try:
                value = float(value)
            except ValueError:
                raise Invalid(u"必须为数字")
        # logger.info("value --> %s, value < 0: %s" % (value, (value < 0)))
        if value < 0:
            raise ValueInvalid(u'必须为大于等于0的数字')
        return value

    @thrownException
    def get_env_resource_fee(self):
        env_id = self.params.get("env_id")
        env = self.db.query(
            Env_Resource_Fee
        ).filter(
            Env_Resource_Fee.env_id == env_id
        ).first()
        return self.success(data=env)

    @thrownException
    def get_or_create(self):
        logger.info("------[get_or_create]------")
        param_schema = Schema({
            "computer": self.validate_float,
            "cpu": self.validate_float,
            "memory": self.validate_float,
            'disk': self.validate_float,
            'disk_backup': self.validate_float,
            'out_ip': self.validate_float,
            'snapshot': self.validate_float,
            'loadbalance': self.validate_float,
            'internet_ip': self.validate_float,
        }, extra=ALLOW_EXTRA)
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
        env, created = Env_Resource_Fee.get_or_create_obj(db=self.db, env_id=env_id)
        logger.info("&" * 60)
        logger.info(env)
        env.computer = computer
        env.cpu = cpu
        env.memory = memory
        env.disk = disk
        env.disk_backup = disk_backup
        env.out_ip = out_ip
        env.snapshot = snapshot
        env.loadbalance = loadbalance
        self.db.add(env)
        self.db.flush()
        return self.success(data=env)
