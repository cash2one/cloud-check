# -*- coding: utf-8 -*-

from sqlalchemy import and_
from scloud.config import logger
from scloud.const import STATUS_RESOURCE
from scloud.models.project import (Pro_Info, Pro_Resource_Apply, get_due_date)

def update_resource_due_date(mapper, connect, target):
    logger.info("\t [update_resource_due_date]")
    logger.info("\t [start_date]:%s" % target.start_date)
    logger.info("\t [period]:%s" % target.period)
    due_date = get_due_date(target.start_date, target.period)
    logger.info("\t due_date: %s" % due_date)
    if due_date:
        connect.execute(
            Pro_Resource_Apply.__table__.update().where(
                    Pro_Resource_Apply.__table__.c.id == target.id
                ).values(
                    due_date = due_date
                )
            )

def update_pro_info_last_apply(mapper, connect, target):
    # applies = connect.execute(
    #     Pro_Resource_Apply.__table__.select().where(
    #         Pro_Resource_Apply.__table__.c.pro_id == target.pro_id
    #     ).order_by(
    #         Pro_Resource_Apply.__table__.c.id.desc()
    #     )
    # )
    # logger.info(applies)
    connect.execute(
        Pro_Info.__table__.update().where(
            Pro_Info.__table__.c.id == target.pro_id
        ).values(
            last_apply_id = target.id
        )
    )

def recover_pro_info_last_apply(mapper, connect, target):
    if target.is_enable == 0:
        logger.info("recover_pro_info_last_apply")
        applies = connect.execute(
            Pro_Resource_Apply.__table__.select().where(
                and_(
                    Pro_Resource_Apply.__table__.c.pro_id == target.pro_id,
                    Pro_Resource_Apply.__table__.c.is_enable == 1
                )
            ).order_by(
                Pro_Resource_Apply.__table__.c.id.desc()
            )
        )
        logger.info(applies)
        if applies.rowcount > 0:
            last_apply = applies.first()
            logger.info(last_apply)
            last_apply_id = last_apply.id
        else:
            last_apply_id = 0
        connect.execute(
            Pro_Info.__table__.update().where(
                Pro_Info.__table__.c.id == target.pro_id
            ).values(
                last_apply_id = last_apply_id
            )
        )
        # from code import interact
        # interact(local=locals())
