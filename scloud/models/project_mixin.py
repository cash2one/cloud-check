# -*- coding: utf-8 -*-

from __future__ import division
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types


class Pro_Info_Mixin(object):

    def get_apply_global_vars(self):
        if hasattr(self, "_get_apply_global_vars"):
            return self._get_apply_global_vars
        logger.info("------[get_last_apply_global_vars]------")
        # logger.info("%s --> %s" % (self.id, self.name))
        last_apply = self.last_apply
        apply_status = last_apply.status if last_apply else None
        percent_status = apply_status + 1 if apply_status else 0
        if percent_status < 0:
            percent_status = 0
        # applies = self.pro_resource_applies
        # if len(applies) > 0:
        #     last_apply = applies[-1]
        #     # logger.info("applies --> %s" % (last_apply))
        #     apply_status = last_apply.status
        #     percent_status = apply_status + 1
        #     if percent_status < 0:
        #         percent_status = 0
        #     # else:
        #     #     last_apply = None
        #     #     apply_status = None
        #     #     percent_status = 0
        # else:
        #     last_apply = None
        #     apply_status = None
        #     percent_status = 0
        progress_percent = '%d%%' % ((percent_status / 4) * 100)
        status_desc = pro_resource_apply_status_types.get(apply_status).value
        todo_status_desc = pro_resource_apply_status_types.get(apply_status).todo_value
        bg_color = pro_resource_apply_status_types.get(apply_status).bg_color
        level = pro_resource_apply_status_types.get(apply_status).level
        data = dict(
            last_apply = last_apply,
            apply_status = apply_status,
            percent_status = percent_status,
            progress_percent = progress_percent,
            status_desc = status_desc,
            todo_status_desc = todo_status_desc,
            bg_color = bg_color,
            level = level,
        )
        # logger.info(data)
        setattr(self, "_get_apply_global_vars", data)
        return self._get_apply_global_vars
        # return data

    @property
    def last_apply(self):
        if hasattr(self, "_last_apply"):
            return self._last_apply
        applies = self.pro_resource_applies
        # logger.info(applies)
        if len(applies) > 0:
            _last_apply = applies[-1]
        else:
            _last_apply = None
        setattr(self, '_last_apply', _last_apply)
        return self._last_apply


class Pro_Resource_Apply_Mixin(object):

    def get_global_vars(self):
        if hasattr(self, "_get_global_vars"):
            return self._get_global_vars
        logger.info("------[get_apply_global_vars]------")
        apply_status = self.status
        percent_status = apply_status + 1
        if percent_status < 0:
            percent_status = 0
        progress_percent = '%d%%' % ((percent_status / 4) * 100)
        status_desc = pro_resource_apply_status_types.get(apply_status).value
        todo_status_desc = pro_resource_apply_status_types.get(apply_status).todo_value
        bg_color = pro_resource_apply_status_types.get(apply_status).bg_color
        level = pro_resource_apply_status_types.get(apply_status).level
        data = dict(
            last_apply = self,
            apply_status = apply_status,
            percent_status = percent_status,
            progress_percent = progress_percent,
            status_desc = status_desc,
            todo_status_desc = todo_status_desc,
            bg_color = bg_color,
            level = level,
        )
        setattr(self,"_get_global_vars", data)
        return self._get_global_vars
        # return data

