# -*- coding: utf-8 -*-

from datetime import datetime
# from tornado import gen
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
# from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.const import STATUS_PRO_TABLES
from scloud.models.project import Pro_Publish
from scloud.models.pt_user import PT_User


class ApplyPublish(BaseService):

    @thrownException
    def get_publish(self):
        logger.info("------get_publish------")
        conditions = and_()

        pro_id = self.params.get("pro_id")
        if pro_id:
            conditions.append(Pro_Publish.pro_id == pro_id)
        id = self.params.get("id")
        if id:
            conditions.append(Pro_Publish.id == id)
        publish = self.db.query(
            Pro_Publish
        ).filter(
            conditions
        ).first()
        return self.success(data=publish)

    @thrownException
    def get_list(self):
        pro_id = self.params.get("pro_id")
        search = self.params.get("search", "")
        status = self.params.get("status", -3)
        conditions = and_()
        user_id = self.params.get("user_id")
        if user_id:
            pt_user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id
            ).first()
            if pt_user and not pt_user.imchecker:
                conditions.append(Pro_Publish.user_id == user_id)
        if pro_id:
            conditions.append(Pro_Publish.pro_id == pro_id)
        if search:
            conditions.append(Pro_Publish.title.like('%' + search + '%'))
        if status > -3:
            conditions.append(Pro_Publish.status == status)
        publish_list = self.db.query(
            Pro_Publish
        ).filter(
            conditions
        ).all()
        return self.success(data=publish_list)

    @thrownException
    def do_publish(self):
        publish_id = self.params.get("publish_id")
        pro_id = self.params.get("pro_id")
        domain = self.params.get("domain")
        domain_port = self.params.get("domain_port")
        network_address = self.params.get("network_address")
        # try:
        #     network_port = int(self.params.get("network_port"))
        # except ValueError:
        #     return self.failure(ERROR.pro_publish_network_port_invalid_err)
        use_ssl = self.params.get("use_ssl", 0)

        # if not pro_id:
        #     return self.failure(ERROR.pro_id_empty_err)
        try:
            pro_id = int(pro_id)
            if not pro_id:
                return self.failure(ERROR.pro_id_empty_err)
        except ValueError:
            return self.failure(ERROR.pro_id_empty_err)
        if not domain:
            return self.failure(ERROR.pro_publish_domain_empty_err)
        if not domain_port:
            return self.failure(ERROR.pro_publish_domain_port_empty_err)
        try:
            domain_port = int(domain_port)
        except ValueError:
            return self.failure(ERROR.pro_publish_domain_port_invalid_err)
        if not network_address:
            return self.failure(ERROR.pro_publish_network_address_empty_err)
        # if not network_port:
        #     return self.failure(ERROR.pro_publish_network_port_empty_err)
        if domain_port < 80 or domain_port > 65535:
            return self.failure(ERROR.pro_publish_domain_port_invalid_err)
        # if network_port < 1024 or network_port > 65535:
        #     return self.failure(ERROR.pro_publish_network_port_invalid_err)
        if publish_id:
            do_publish_info = self.db.query(
                Pro_Publish
            ).filter(
                Pro_Publish.id == publish_id
            ).first()
        do_publish_info = Pro_Publish()
        do_publish_info.pro_id = pro_id
        do_publish_info.domain = domain
        do_publish_info.domain_port = domain_port
        do_publish_info.network_address = network_address
        # do_publish_info.network_port = network_port
        do_publish_info.use_ssl = use_ssl
        do_publish_info.status = STATUS_PRO_TABLES.APPLIED
        do_publish_info.user_id = self.handler.current_user.id
        self.db.add(do_publish_info)
        self.db.flush()
        return self.success(data=do_publish_info)

    @thrownException
    def do_del_pro_publish(self):
        id_list = self.params.get("id_list")
        for id in id_list:
            pro_publish = self.db.query(
                Pro_Publish
            ).filter(
                Pro_Publish.id == id    
            ).first()
            self.db.delete(pro_publish)
            self.db.flush()
        return self.success(data=None)
