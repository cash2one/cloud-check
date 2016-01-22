
from scloud.config import logger
from scloud.models.project import (Pro_Info, Pro_Resource_Apply)
from scloud.models.environment import (Env_Info,
    Env_Resource_Value, Env_Resource_Fee,
    Env_Internet_Ip_Types)
from scloud.models.pt_user import PT_Perm
from scloud.models.act import Act_Todo
from sqlalchemy import event, func
from scloud.async_services.svc_act import task_act_post
from scloud.async_services.base import thrownException


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


def update_keycode(mapper, connect, target):
    connect.execute(
        PT_Perm.__table__.update().where(
                PT_Perm.__table__.c.id == target.id
            ).values(
                keycode = u"1%.3d" % (target.id)
            )
        )
    # connect.commit()


def init_listener():
    init_after_insert()
    init_after_update()
    init_after_delete()


def init_after_insert():
    event.listen(Act_Todo, 'after_insert', act_post)
    event.listen(Pro_Info, 'after_insert', act_post)
    event.listen(Pro_Resource_Apply, 'after_insert', act_post)
    event.listen(Env_Info, 'after_insert', act_post)
    event.listen(Env_Resource_Fee, 'after_insert', act_post)
    event.listen(Env_Resource_Value, 'after_insert', act_post)
    event.listen(Env_Internet_Ip_Types, 'after_insert', act_post)
    event.listen(PT_Perm, 'after_insert', act_post)
    event.listen(PT_Perm, 'after_insert', update_keycode)


def init_after_update():
    event.listen(Act_Todo, 'after_update', act_update)
    event.listen(Pro_Info, 'after_update', act_update)
    event.listen(Pro_Resource_Apply, 'after_update', act_post)
    event.listen(Env_Info, 'after_update', act_post)
    event.listen(Env_Resource_Fee, 'after_update', act_post)
    event.listen(Env_Resource_Value, 'after_update', act_post)
    event.listen(Env_Internet_Ip_Types, 'after_update', act_post)
    event.listen(PT_Perm, 'after_update', act_post)


def init_after_delete():
    event.listen(Act_Todo, 'after_delete', act_delete)
    event.listen(Pro_Info, 'after_delete', act_delete)
    event.listen(Pro_Resource_Apply, 'after_delete', act_post)
    event.listen(Env_Info, 'after_delete', act_post)
    event.listen(Env_Resource_Fee, 'after_delete', act_post)
    event.listen(Env_Resource_Value, 'after_delete', act_post)
    event.listen(Env_Internet_Ip_Types, 'after_delete', act_post)
    event.listen(PT_Perm, 'after_delete', act_post)
