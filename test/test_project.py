# -*- coding: utf-8 -*-

import uuid
from os.path import abspath, dirname, join
current_path = abspath(dirname(__file__))
import sys
sys.path.insert(0, join(current_path, '..', "scloud"))
# sys.path.insert(0, join(current_path, '..'))
from scloud.config import logger
# from scloud.async_services.listener import init_listener
from scloud.models.base import DataBaseService
from scloud.models.project import Pro_Info
from scloud.services.svc_project import ProjectService

#init_listener()


if __name__ == '__main__':
    logger.info("-----[0 post_act_history]------")
    # try:
    dbsvc = DataBaseService({})
    dbsvc._db_init()
    svc = ProjectService(dbsvc, {"env": 2, "status": ""})
    svc.filter_list()
