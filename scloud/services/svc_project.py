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


class ProjectService(BaseService):

    @thrownException
    def get_project(self):
        logger.info("------[get_project]------")
        pro_id = self.params.get("pro_id", 0)
        project = self.db.query(Pro_Info).filter(Pro_Info.id == pro_id).first()
        if project:
            res = project.as_dict()
            logger.info("project: %s" % res)
            return self.success(data=project)
        else:
            return NotFoundError()

    @thrownException
    def get_project_list(self):
        logger.info("------[get_project_list]------")
        projects = self.db.query(Pro_Info).all()
        project_list = [i.as_dict() for i in projects]
        logger.info("project_list %s" % project_list)
        # self.db.commit()
        # self.db.remove()
        return self.success(data=project_list)

    @thrownException
    def create_project(self):
        name = self.params.get("name", "").strip()
        owner = self.params.get("owner", "").strip()
        owner_email = self.params.get("owner_email", "").strip()
        env_id = self.params.get("env_id", "").strip()
        desc = self.params.get("desc", "").strip()
        if not name:
            return self.failure(ERROR.pro_name_empty_err)
        if not owner:
            return self.failure(ERROR.pro_owner_empty_err)
        # if not owner_email:
        #     return self.failure(ERROR.pro_owner_email_empty_err)
        if not env_id:
            return self.failure(ERROR.pro_env_empty_err)
        project, created = Pro_Info.get_or_create(name=name, owner=owner, env_id=env_id)
        project.owner_email = owner_email
        project.desc = desc
        self.db.add(project)
        return self.success(data=project)
