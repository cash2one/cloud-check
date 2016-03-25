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
from scloud.models.project import Pro_Publish, Pro_Balance 


class ApplyPublish(BaseService):

    @thrownException
    def get_publish(self):
        pro_id = self.params.get("pro_id")
        publish = self.db.query(
            Pro_Publish
        ).filter(
            Pro_Publish.pro_id == pro_id
        ).first()
        return self.success(data=publish)

    @thrownException
    def do_publish(self):
        pro_id = self.params.get("pro_id")
        domain = self.params.get("domain")
        try:
            domain_port = int(self.params.get("domain_port"))
        except ValueError:
            return self.failure(ERROR.pro_publish_domain_port_invalid_err)

        network_address = self.params.get("network_address")
        try:
            network_port = int(self.params.get("network_port"))
        except ValueError:
            return self.failure(ERROR.pro_publish_network_port_invalid_err)
        use_ssl = self.params.get("use_ssl", 0)

        if not pro_id:
            return self.failure(ERROR.not_found_err) 
        if not domain:
            return self.failure(ERROR.pro_publish_domain_empty_err)
        if not domain_port:
            return self.failure(ERROR.pro_publish_domain_port_empty_err)
        if not network_address:
            return self.failure(ERROR.pro_publish_network_address_empty_err)
        if not network_port:
            return self.failure(ERROR.pro_publish_network_port_empty_err)
        if domain_port < 80 or domain_port > 65535:
            return self.failure(ERROR.pro_publish_domain_port_invalid_err)
        if network_port < 1024 or network_port > 65535:
            return self.failure(ERROR.pro_publish_network_port_invalid_err)
        do_publish_info, created = Pro_Publish.get_or_create_obj(self.db, pro_id=pro_id) 
        do_publish_info.domain = domain
        do_publish_info.domain_port = domain_port
        do_publish_info.network_address = network_address
        do_publish_info.network_port = network_port
        do_publish_info.use_ssl = use_ssl
        self.db.add(do_publish_info)
        return self.success(data=do_publish_info) 



        



        


        



        



