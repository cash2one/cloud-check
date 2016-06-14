# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info, Pro_Resource_Apply
from scloud.models.environment import Env_Resource_Value, Env_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_, func
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types
from tornado.util import ObjectDict


class ProjectService(BaseService):

    @thrownException
    def load_env_resource_values(self):
        logger.info("------[load_env_resource_values]------")
        pro_id = self.params.get("pro_id", 0)
        project = self.db.query(Pro_Info).filter(Pro_Info.id == pro_id).first()
        if project:
            env_resource_value = project.env.env_resource_value
            return self.success(data=env_resource_value.as_dict() if env_resource_value else {})
        else:
            return self.failure(ERROR.not_found_err)

    @thrownException
    def load_env_internet_ip_types(self):
        logger.info("------[load_env_internet_ip_types]------")
        pro_id = self.params.get("pro_id", 0)
        project = self.db.query(Pro_Info).filter(Pro_Info.id == pro_id).first()
        if project:
            internet_ip_types = project.env.env_internet_ip_types
            internet_ip_options = [{"value": i.id, "desc": i.name, "bandwidths": i.bandwidths} for i in internet_ip_types]
            return self.success(data=internet_ip_options)
        else:
            return self.failure(ERROR.not_found_err)

    @thrownException
    def get_project(self):
        logger.info("------[get_project]------")
        pro_id = self.params.get("pro_id", 0)
        if not pro_id:
            return self.failure(ERROR.pro_id_empty_err)
        project = self.db.query(Pro_Info).filter(Pro_Info.id == pro_id).first()
        if project:
            # res = project.as_dict()
            # logger.info("project: %s" % res)
            return self.success(data=project)
        else:
            return self.failure(ERROR.not_found_err)
            # return NotFoundError()

    @thrownException
    def get_project_list(self):
        logger.info("------[get_project_list]------")
        user_id = self.handler.current_user.id
        projects = self.db.query(
            Pro_Info
        ).filter(
            Pro_Info.user_id == user_id
        ).all()
        # project_list = [i.as_dict() for i in projects]
        # logger.info("project_list %s" % project_list)
        # self.db.commit()
        # self.db.remove()
        return self.success(data=projects)

    @thrownException
    def create_project(self):
        name = self.params.get("name", "").strip()
        user_id = self.handler.current_user.id
        owner = self.params.get("owner", "").strip()
        owner_email = self.params.get("owner_email", "").strip()
        env_id = self.params.get("env_id", "").strip()
        desc = self.params.get("desc", "").strip()
        if not name:
            return self.failure(ERROR.pro_name_empty_err)
        if not owner:
            return self.failure(ERROR.pro_owner_empty_err)
        if not owner_email:
            return self.failure(ERROR.pro_owner_email_empty_err)
        if not env_id:
            return self.failure(ERROR.pro_env_empty_err)
        project, created = Pro_Info.get_or_create_obj(self.db, name=name, owner=owner, env_id=env_id)
        project.owner_email = owner_email
        project.desc = desc
        project.user_id = user_id
        self.db.add(project)
        self.db.flush()
        return self.success(data=project)

    @thrownException
    def filter_list(self):
        conditions = and_()
        env = self.params.get("env")
        status = self.params.get("status")
        if env:
            conditions.append(Pro_Info.env_id == env)
        if status:
            conditions.append(Pro_Resource_Apply.status == status)
        projects = self.db.query(
            Pro_Info
        ).outerjoin(
            Pro_Resource_Apply, Pro_Info.last_apply_id == Pro_Resource_Apply.id
        ).filter(
            conditions
        ).order_by(
            Pro_Info.id.desc()
        ).all()
        # project_list = [i.as_dict() for i in projects]
        # logger.info("project_list %s" % project_list)
        # self.db.commit()
        # self.db.remove()
        projects_by_env = self.db.query(
            Env_Info.id, Env_Info.name, func.count(Pro_Info.id)
        ).outerjoin(
            Pro_Info, Env_Info.id == Pro_Info.env_id
        ).group_by(
            Env_Info.id
        ).all()
        logger.info(projects_by_env)

        projects_by_status = self.db.query(
            Pro_Resource_Apply.status, func.count(Pro_Info.id)
        ).outerjoin(
            Pro_Info, Pro_Resource_Apply.id == Pro_Info.last_apply_id
        ).group_by(
            Pro_Resource_Apply.status
        ).all()
        logger.info(projects_by_status)
        data = ObjectDict()
        data.projects = projects
        data.projects_by_env = projects_by_env
        data.projects_by_status = projects_by_status
        return self.success(data=data)
