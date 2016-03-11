#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from os.path import abspath, dirname, join
current_path = abspath(dirname(__file__))
import sys
sys.path.insert(0, join(current_path, "scloud"))
from scloud.config import logger
from scloud.models.base import DataBaseService, db_engine, BaseModel
from scloud.models.environment import (
    Env_Info,
    Env_Internet_Ip_Types,
    Env_Resource_Value,
    Env_Resource_Fee
)

if __name__ == '__main__':
    logger.info("start create ...")
    BaseModel.metadata.create_all(db_engine)
    logger.info("create finished")
