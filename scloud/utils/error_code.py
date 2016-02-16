# -*- coding: utf-8 -*-

from collections import namedtuple

error = namedtuple("operate", ["errvalue", "errcode"])


class ERROR(object):
    system_err = error(errcode=-999999, errvalue=u"系统错误")
    # 注册和登录
    username_empty_err = error(errcode=-100001, errvalue=u"用户名不能为空")
    username_err       = error(errcode=-100002, errvalue=u"该用户名不存在")
    password_empty_err = error(errcode=-100003, errvalue=u"密码不能为空")
    password_err       = error(errcode=-100004, errvalue=u"密码错误")
    email_empty_err    = error(errcode=-100005, errvalue=u"邮箱不能为空")
    email_err          = error(errcode=-100006, errvalue=u"邮箱错误")
    mobile_empty_err   = error(errcode=-100007, errvalue=u"手机号不能为空")
    mobile_err         = error(errcode=-100008, errvalue=u"手机号错误")

    # 创建项目
    pro_name_empty_err = error(errcode=-100020, errvalue=u"项目名称不能为空")
    pro_owner_empty_err = error(errcode=-100021, errvalue=u"项目负责人不能为空")
    pro_owner_email_empty_err = error(errcode=-100022, errvalue=u"项目负责人邮箱不能为空")
    pro_env_empty_err = error(errcode=-100023, errvalue=u"项目环境不能为空")


if __name__ == '__main__':
    print ERROR.username_err.keycode, ERROR.username_err.value
