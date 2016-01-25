#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import logger, thrownException
from scloud.celeryapp import celery
from scloud.models.pt_user import PT_Role
from scloud.models.base import DataBaseService
from sqlalchemy import or_, and_


@celery.task
@thrownException
def get_list(search=""):
    with DataBaseService({}) as svc:
        or_conditions = or_()
        or_conditions.append(PT_Role.name.like("%" + search + "%"))
        or_conditions.append(PT_Role.desc.like("%" + search + "%"))
        or_conditions.append(PT_Role.remark.like("%" + search + "%"))
        pt_roles = svc.db.query(
            PT_Role
        ).filter(
            or_conditions
        ).order_by(
            PT_Role.id.desc()
        ).all()
        pt_roles = [i.as_dict() for i in pt_roles]
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": pt_roles
        }
    return data


@celery.task
@thrownException
def get_info(perm_id):
    with DataBaseService({}) as svc:
        pt_role = svc.db.query(
            PT_Role
        ).filter(
            PT_Role.id == perm_id
        ).one()
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": pt_role.as_dict()
        }
    return data


@celery.task
@thrownException
def get_or_create(name, desc=u"", remark=u""):
    role_info, created = PT_Role.get_or_create(
        name = name,
        )
    role_info.desc = desc
    role_info.remark = remark
    with DataBaseService({}) as svc:
        svc.db.add(role_info)
    data = {
            "return_code": 0,
            "return_message": u"",
            "data": role_info.as_dict()
        }
    return data


@celery.task
@thrownException
def update_info(role_id, name=u"", desc=u"", remark=u""):
    with DataBaseService({}) as svc:
        role = svc.db.query(
            PT_Role
        ).filter(
            PT_Role.id == role_id,
        ).one()
        role.name = name
        role.desc = desc
        role.remark = remark
        svc.db.add(role)
    data = {
            "return_code": 0,
            "return_message": u"",
            "data": role.as_dict()
        }
    return data
