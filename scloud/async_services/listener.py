
from scloud.config import logger
from scloud.models.project import Pro_Info
from sqlalchemy import event
from scloud.async_services.svc_act import (task_act_post)


def act_post(mapper, connect, target):
    logger.info("-----[after_insert act_post]------")
    logger.info(target.__class__.__name__)
    logger.info(target.__doc__)
    task_act_post.delay(act_type=1, table_name=target.__class__.__name__, table_doc=target.__doc__)


def act_update(mapper, connect, target):
    logger.info("-----[after_insert act_post2]------")
    logger.info(target.__class__.__name__)
    logger.info(target.__doc__)
    task_act_post.delay(act_type=2, table_name=target.__class__.__name__, table_doc=target.__doc__)


def act_delete(mapper, connect, target):
    logger.info("-----[after_insert act_post2]------")
    logger.info(target.__class__.__name__)
    logger.info(target.__doc__)
    task_act_post.delay(act_type=3, table_name=target.__class__.__name__, table_doc=target.__doc__)


def init_listener():
    init_after_insert()
    init_after_update()
    init_after_delete()


def init_after_insert():
    event.listen(Pro_Info, 'after_insert', act_post)


def init_after_update():
    event.listen(Pro_Info, 'after_update', act_update)


def init_after_delete():
    event.listen(Pro_Info, 'after_delete', act_delete)
