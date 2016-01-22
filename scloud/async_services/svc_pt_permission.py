#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import logger, thrownException
from scloud.celeryapp import celery
from scloud.models.pt_user import PT_Perm
from scloud.models.base import DataBaseService
from sqlalchemy import or_, and_


@celery.task
@thrownException
def get_list(search=""):
    with DataBaseService({}) as svc:
        or_conditions = or_()
        or_conditions.append(PT_Perm.name.like("%" + search + "%"))
        or_conditions.append(PT_Perm.keyword.like("%" + search + "%"))
        or_conditions.append(PT_Perm.keycode.like("%" + search + "%"))
        pt_perms = svc.db.query(
            PT_Perm
        ).filter(
            or_conditions
        ).order_by(
            PT_Perm.id.desc()
        ).all()
        pt_perms = [i.as_dict() for i in pt_perms]
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": pt_perms
        }
    return data


@celery.task
@thrownException
def get_info(perm_id):
    with DataBaseService({}) as svc:
        pt_perm = svc.db.query(
            PT_Perm
        ).filter(
            PT_Perm.id == perm_id
        ).one()
        data = {
            "return_code": 0,
            "return_message": u"",
            "data": pt_perm.as_dict()
        }
    return data


@celery.task
@thrownException
def get_or_create(name, keyword):
    perm_info, created = PT_Perm.get_or_create(
        name = name,
        keyword = keyword,
        )
    data = {
            "return_code": 0,
            "return_message": u"",
            "data": perm_info.as_dict()
        }
    return data


@celery.task
@thrownException
def update(perm_id, name, keyword, keycode):
    with DataBaseService({}) as svc:
        is_success = svc.db.query(
            PT_Perm
        ).filter(
            PT_Perm.id == perm_id,
        ).update(
            {
                PT_Perm.name: name,
                PT_Perm.keyword: keyword,
                PT_Perm.keycode: keycode,
            }
        )
    return is_success
