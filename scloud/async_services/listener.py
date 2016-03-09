# -*- coding: utf-8 -*-

import simplejson
from datetime import datetime
from scloud.config import logger
from scloud.models.project import (Pro_Info, Pro_Resource_Apply, get_due_date)
from scloud.models.environment import (Env_Info,
    Env_Resource_Value, Env_Resource_Fee,
    Env_Internet_Ip_Types)
from scloud.models.pt_user import PT_Perm, PT_Role, PT_Role_Group_Ops
from scloud.models.act import Act_Todo
from scloud.models.environment import Env_Internet_Ip_Types, Env_Resource_Fee
from sqlalchemy import event, func, select
from scloud.async_services.svc_act import task_act_post
from scloud.config import thrownException


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

def get_or_create_env_resource_fee(mapper, connect, target):
    env_internet_ip_types = connect.execute(Env_Internet_Ip_Types.__table__.select().where(
        Env_Internet_Ip_Types.__table__.c.env_id == target.env_id
    ))
    env_internet_ip_types = [{"id": i.id, "name": i.name, "fee": "%.2f" % i.fee} for i in env_internet_ip_types]
    result = connect.execute(
        Env_Resource_Fee.__table__.update().where(
            Env_Resource_Fee.env_id == target.env_id
        ).values(
            internet_ip = simplejson.dumps(env_internet_ip_types)
        )
    )
    logger.info(result.rowcount)
    # from code import interact
    # interact(local=locals())
    if result.rowcount <= 0:
        insert_result = connect.execute(
            Env_Resource_Fee.__table__.insert().values(
                env_id = target.env_id,
                internet_ip = simplejson.dumps(env_internet_ip_types)
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
    event.listen(Env_Internet_Ip_Types, 'after_insert', get_or_create_env_resource_fee)
    event.listen(PT_Perm, 'after_insert', act_post)
    event.listen(PT_Perm, 'after_insert', update_keycode)
    event.listen(PT_Role, 'after_insert', act_post)
    event.listen(PT_Role_Group_Ops, 'after_insert', act_post)


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


def init_after_delete():
    event.listen(Act_Todo, 'after_delete', act_delete)
    event.listen(Pro_Info, 'after_delete', act_delete)
    event.listen(Pro_Resource_Apply, 'after_delete', act_delete)
    event.listen(Env_Info, 'after_delete', act_delete)
    event.listen(Env_Resource_Fee, 'after_delete', act_delete)
    event.listen(Env_Resource_Value, 'after_delete', act_delete)
    event.listen(Env_Internet_Ip_Types, 'after_delete', act_delete)
    event.listen(PT_Perm, 'after_delete', act_delete)
    event.listen(PT_Role, 'after_delete', act_delete)
    event.listen(PT_Role_Group_Ops, 'after_delete', act_delete)
