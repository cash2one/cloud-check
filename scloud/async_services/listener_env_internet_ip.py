# -*- coding: utf-8 -*-

import simplejson
from scloud.config import logger
from scloud.models.environment import (
    Env_Info,
    Env_Internet_Ip_Types,
    Env_Internet_Bandwidth,
    Env_Resource_Fee,
    Env_Resource_Value
)

def get_or_create_env_resource_fee(mapper, connect, target):
    logger.error("\t !!![get_or_create_env_resource_fee]")
    logger.error("\t target id:%s" % target.id)
    if target.env_id != 0:
        env_internet_ip_types = connect.execute(
            Env_Internet_Ip_Types.__table__.select().where(
                Env_Internet_Ip_Types.__table__.c.env_id == target.env_id
            )
        )
        _env_internet_ip_types = []
        for internet_ip_type in env_internet_ip_types:
            _json_obj = dict(id=internet_ip_type.id, name=internet_ip_type.name)
            bandwidth_list = connect.execute(
                Env_Internet_Bandwidth.__table__.select().where(
                    Env_Internet_Bandwidth.__table__.c.internet_ip_type_id == internet_ip_type.id
                )
            )
            _bandwidth_obj = {bw.bandwidth_id: bw.fee for bw in bandwidth_list}
            _json_obj.update(fee=_bandwidth_obj)
            _env_internet_ip_types.append(_json_obj)
        # env_internet_ip_types = [{"id": i.id, "name": i.name, "fee": "%.2f" % i.fee} for i in env_internet_ip_types]
        result = connect.execute(
            Env_Resource_Fee.__table__.update().where(
                Env_Resource_Fee.env_id == target.env_id
            ).values(
                internet_ip = simplejson.dumps(_env_internet_ip_types)
            )
        )
        logger.info(result.rowcount)
        # from code import interact
        # interact(local=locals())
        if result.rowcount <= 0:
            if target.env_id:
                insert_result = connect.execute(
                    Env_Resource_Fee.__table__.insert().values(
                        env_id = target.env_id,
                        internet_ip = simplejson.dumps(_env_internet_ip_types)
                    )
                )
                logger.info(insert_result.rowcount)
        logger.info("\t [env_internet_ip_types]: %s" % env_internet_ip_types)
    # logger.info("\t [update_resource_due_date]")
    # logger.info("\t [start_date]:%s" % target.start_date)
    # logger.info("\t [period]:%s" % target.period)
    # due_date = get_due_date(target.start_date, target.period)
    # logger.info("\t due_date: %s" % due_date)
    # if due_date:
    #     connect.execute(
    #         Pro_Resource_Apply.__table__.update().where(
    #                 Pro_Resource_Apply.__table__.c.id == target.id
    #             ).values(
    #                 due_date = due_date
    #             )
    #         )
