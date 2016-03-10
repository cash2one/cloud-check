# -*- coding: utf-8 -*-

import simplejson
from datetime import datetime
from scloud.config import logger
from scloud.models.project import (Pro_Info, Pro_Resource_Apply)
from scloud.models.environment import (Env_Info,
    Env_Resource_Value, Env_Resource_Fee,
    Env_Internet_Ip_Types)
from scloud.models.pt_user import PT_Perm, PT_Role, PT_Role_Group_Ops
from scloud.models.act import Act_Todo
# from scloud.models.environment import Env_Internet_Ip_Types, Env_Resource_Fee, Env_Resource_Value
from sqlalchemy import event, func, select
from scloud.async_services.svc_act import task_act_post
from scloud.config import thrownException
from scloud.async_services.listener_env_info import delete_env_info
from scloud.async_services.listener_env_internet_ip import get_or_create_env_resource_fee
from scloud.async_services.listener_pro_resource_apply import update_resource_due_date


def act_post(mapper, connect, target):
    pass
    # logger.info("-----[after_insert act_post]------")
    # logger.info(target.__class__.__name__)
    # logger.info(target.__doc__)
    # task_act_post.delay(act_type=1, table_name=target.__class__.__name__, table_doc=target.__doc__)


def act_update(mapper, connect, target):
    # logger.info("-----[after_update act_post]------")
    # logger.info(target.__class__.__name__)
    # logger.info(target.__doc__)
    connect.execute(
        target.__table__.update().where(
                target.__table__.c.id == target.id
            ).values(
                update_time = datetime.now()
            )
        )
    # task_act_post.delay(act_type=2, table_name=target.__class__.__name__, table_doc=target.__doc__)


def act_delete(mapper, connect, target):
    pass
    # logger.info("-----[after_delete act_post]------")
    # logger.info(target.__class__.__name__)
    # logger.info(target.__doc__)
    # task_act_post.delay(act_type=3, table_name=target.__class__.__name__, table_doc=target.__doc__)


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
    #init_before_delete()


def init_after_insert():
    event.listen(Env_Internet_Ip_Types, 'after_insert', get_or_create_env_resource_fee)


def init_after_update():
    event.listen(Act_Todo, 'after_update', act_update)
    event.listen(Pro_Info, 'after_update', act_update)
    event.listen(Pro_Resource_Apply, 'after_update', act_update)
    event.listen(Pro_Resource_Apply, 'after_update', update_resource_due_date)
    event.listen(Env_Info, 'after_update', act_update)
    event.listen(Env_Resource_Fee, 'after_update', act_update)
    event.listen(Env_Resource_Value, 'after_update', act_update)
    event.listen(Env_Internet_Ip_Types, 'after_update', act_update)
    event.listen(Env_Internet_Ip_Types, 'after_update', get_or_create_env_resource_fee)
    event.listen(PT_Perm, 'after_update', act_update)
    event.listen(PT_Role, 'after_update', act_update)
    event.listen(PT_Role_Group_Ops, 'after_update', act_update)


def init_before_delete():
    event.listen(Env_Info, 'before_delete', delete_env_info)
