# -*- coding: utf-8 -*-

from scloud.config import logger
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
