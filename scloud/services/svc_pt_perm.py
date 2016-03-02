# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types


class PtPermService(BaseService):

    @thrownException
    def get_list(self):
        logger.info("------[get_list]------")
        search = self.params.get("search", "")
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
        return self.success(data=project)

    @thrownException
    def get_info(self):
        logger.info("------[get_info]------")
        perm_id = self.params.get("perm_id")
        pt_perm = svc.db.query(
            PT_Perm
        ).filter(
            PT_Perm.id == perm_id
        ).first()
        if pt_perm:
            return self.success(data=projects)
        else:
            return NotFoundError()

    @thrownException
    def get_or_create(self):
        logger.info("------ [get_or_create] ------")
        name = self.params.get("name", "")
        keyword = self.params.get("keyword", "")
        perm_info, created = PT_Perm.get_or_create(
            name = name,
            keyword = keyword,
            )
        return self.success(data=perm_info)

    @thrownException
    def update_info(self):
        logger.info("------ [update_info] ------")
        perm_id = self.params.get("perm_id")
        name = self.params.get("name", "")
        keyword = self.params.get("keyword", "")

        perm = svc.db.query(
            PT_Perm
        ).filter(
            PT_Perm.id == perm_id,
        ).one()
        perm.name = name
        perm.keyword = keyword
        svc.db.add(perm)
        return self.success(data={"is_success": True})
