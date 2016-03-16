# -*- coding: utf-8 -*-

from __future__ import division
from scloud.config import logger, thrownException

class PT_User_Mixin(object):

    def get_current_perms(self):
        from scloud.utils.permission import GROUP, OP
        logger.info("------[get_last_apply_global_vars]------")
        if hasattr(self, "current_perms"):
            return getattr(self, "current_perms")
        user_roles = self.user_roles
        current_perms = {}
        for user_role in user_roles:
            group_ops = user_role.role.group_ops
            for group_op in group_ops:
                g_keyword = GROUP[group_op.group_keycode].keyword
                op_keyword = OP[group_op.op_keycode].keyword
                g_keycode = group_op.group_keycode
                op_keycode = group_op.op_keycode
                current_perms.update({"%s.%s" % (g_keyword, op_keyword): "%s.%s" % (g_keycode, op_keycode)})
        setattr(self, "current_perms", current_perms)
        return getattr(self, "current_perms")
