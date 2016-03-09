# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.environment import Env_Info, Env_Internet_Ip_Types
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE



class EnvInternetIpService(BaseService):
    @thrownException
    def get_env_internet_ip(self):
        env_internet_ip_id = self.params.get("env_internet_ip_id")
        env_internet_ip = self.db.query(
            Env_Internet_Ip_Types
        ).filter(
            Env_Internet_Ip_Types.id == env_internet_ip_id
        ).first()
        if not env_internet_ip:
            return self.failure(ERROR.not_found_err)
        return self.success(data=env_internet_ip)

    @thrownException
    def add_env_internet_ip(self):
        env_id = self.params.get("env_id")
        name = self.params.get("name")
        try:
            fee = float(self.params.get("fee") or 0)
        except:
            return self.failure(ERROR.env_internet_ip_fee_invalid_err)
        desc = self.params.get("desc")
        env = self.db.query(
            Env_Info
        ).filter(
            Env_Info.id == env_id
        ).first()
        if not env:
            return self.failure(ERROR.not_found_err)
        if not name:
            return self.failure(ERROR.env_internet_ip_name_empty_err)
        env_internet_ip, created = Env_Internet_Ip_Types.get_or_create_obj(self.db, env_id=env_id, name=name)
        if created:
            env_internet_ip.fee = fee
            env_internet_ip.desc = desc
            self.db.add(env_internet_ip)
            return self.success(data=env_internet_ip)
        else:
            return self.failure(ERROR.env_internet_ip_name_duplicate_err)

    @thrownException
    def edit_env_internet_ip(self):
        env_id = self.params.get("env_id")
        env_internet_ip_id = self.params.get("env_internet_ip_id")
        name = self.params.get("name")
        try:
            fee = float(self.params.get("fee") or 0)
        except:
            return self.failure(ERROR.env_internet_ip_fee_invalid_err)
        desc = self.params.get("desc")
        env = self.db.query(
            Env_Info
        ).filter(
            Env_Info.id == env_id
        ).first()
        if not env:
            return self.failure(ERROR.not_found_err)
        if not name:
            return self.failure(ERROR.env_internet_ip_name_empty_err)
        env_internet_ip = self.db.query(
            Env_Internet_Ip_Types
        ).filter(
            Env_Internet_Ip_Types.id != env_internet_ip_id,
            Env_Internet_Ip_Types.env_id == env_id,
            Env_Internet_Ip_Types.name == name
        ).first()
        logger.info(env_internet_ip)
        if env_internet_ip:
            return self.failure(ERROR.env_internet_ip_name_duplicate_err)
        else:
            env_internet_ip = self.db.query(
                Env_Internet_Ip_Types
            ).filter(
                Env_Internet_Ip_Types.id == env_internet_ip_id,
                Env_Internet_Ip_Types.env_id == env_id,
            ).first()
            env_internet_ip.name = name
            env_internet_ip.fee = fee
            env_internet_ip.desc = desc
            self.db.add(env_internet_ip)
            return self.success(data=env_internet_ip)

    @thrownException
    def del_env_internet_ip(self):
        env_internet_ip_ids = self.params.get("env_internet_ip_ids", [])
        # env_internet_ip_ids = [i for i in env_internet_ip_ids if isinstance(i, int)]
        or_conditions = or_()
        for id in env_internet_ip_ids:
            #if isinstance(id, int):
            logger.error(id)
            or_conditions.append(Env_Internet_Ip_Types.id == id)
        ips = self.db.query(
            Env_Internet_Ip_Types
        ).filter(
            or_conditions
        ).all()
        return self.success(data=ips)
