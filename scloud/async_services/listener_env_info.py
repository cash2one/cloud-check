# -*- coding: utf-8 -*-

from scloud.config import logger
from scloud.models.environment import (Env_Info,
                                       Env_Internet_Ip_Types,
                                       Env_Resource_Fee,
                                       Env_Resource_Value)

def delete_env_info(mapper, connect, target):
    logger.error("\t [delete_env_info]")
    logger.error("\t target id:%s" % target.id)
    logger.error("\t target name:%s" % target.name)
    res1 = connect.execute(
        Env_Internet_Ip_Types.__table__.delete().where(
            Env_Internet_Ip_Types.__table__.c.env_id == target.id
        )
    )
    res2 = connect.execute(
        Env_Resource_Fee.__table__.delete().where(
            Env_Resource_Fee.__table__.c.env_id == target.id
        )
    )
    res3 = connect.execute(
        Env_Resource_Value.__table__.delete().where(
            Env_Resource_Value.__table__.c.env_id == target.id
        )
    )
    logger.info("\t res1:%s" % res1.rowcount)
    logger.info("\t res2:%s" % res2.rowcount)
    logger.info("\t res3:%s" % res3.rowcount)
    logger.error("\t [delete_env_info_finish]")
