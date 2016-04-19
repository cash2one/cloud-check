# -*- coding: utf-8 -*-

from scloud.handlers import AuthHandler
from scloud.services.svc_project import ProjectService


class ApplyHandler(AuthHandler):
    def get_pro_data(self, **kw):
        # kw = {"pro_id": pro_id}
        svc = ProjectService(self, kw)
        if "pro_id" in kw:
            pro_info_res = svc.get_project()
            if isinstance(pro_info_res, Exception):
                raise pro_info_res
        pro_list_res = svc.get_project_list()
        data = {
            "pro_list_res": pro_list_res,
        }
        if "pro_id" in kw:
            data.update({"pro_info_res": pro_info_res})
        return data
