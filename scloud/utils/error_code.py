# -*- coding: utf-8 -*-

from collections import namedtuple

error = namedtuple("operate", ["errvalue", "errcode"])


class ERROR(object):
    system_err = error(errcode=-999999, errvalue=u"系统错误")
    not_found_err = error(errcode=-999404, errvalue=u"对不起！您正在访问的数据资源未找到")
    # 注册和登录
    username_empty_err = error(errcode=-100001, errvalue=u"用户名不能为空")
    username_err       = error(errcode=-100002, errvalue=u"该用户名不存在")
    password_empty_err = error(errcode=-100003, errvalue=u"密码不能为空")
    password_err       = error(errcode=-100004, errvalue=u"密码错误")
    email_empty_err    = error(errcode=-100005, errvalue=u"邮箱不能为空")
    email_err          = error(errcode=-100006, errvalue=u"邮箱错误")
    mobile_empty_err   = error(errcode=-100007, errvalue=u"手机号不能为空")
    mobile_err         = error(errcode=-100008, errvalue=u"手机号错误")
    user_empty_err     = error(errcode=-100009, errvalue=u"操作用户不能为空")
    checker_empty_err  = error(errcode=-100010, errvalue=u"审核用户不能为空")

    # 创建项目
    pro_name_empty_err        = error(errcode=-100020, errvalue=u"项目名称不能为空")
    pro_owner_empty_err       = error(errcode=-100021, errvalue=u"项目负责人不能为空")
    pro_owner_email_empty_err = error(errcode=-100022, errvalue=u"项目负责人邮箱不能为空")
    pro_env_empty_err         = error(errcode=-100023, errvalue=u"项目环境不能为空")

    # 创建资源
    res_computer_empty_err        = error(errcode=-100040, errvalue=u"申请云主机不能为空")
    res_cpu_empty_err             = error(errcode=-100041, errvalue=u"申请CPU不能为空")
    res_memory_empty_err          = error(errcode=-100042, errvalue=u"申请内存不能为空")
    res_disk_empty_err            = error(errcode=-100043, errvalue=u"申请云磁盘不能为空")
    res_disk_backup_empty_err     = error(errcode=-100044, errvalue=u"申请云磁盘备份不能为空")
    res_out_ip_empty_err          = error(errcode=-100045, errvalue=u"申请外部IP不能为空")
    res_snapshot_empty_err        = error(errcode=-100046, errvalue=u"申请快照不能为空")
    res_loadbalance_empty_err     = error(errcode=-100047, errvalue=u"申请应用负载均衡不能为空")
    res_internet_ip_empty_err     = error(errcode=-100048, errvalue=u"申请互联网IP不能为空")
    res_internet_ip_ssl_empty_err = error(errcode=-100049, errvalue=u"申请是否需要SSL卸载不能为空")
    res_start_date_empty_err      = error(errcode=-100050, errvalue=u"申请启动时间不能为空")
    res_period_empty_err          = error(errcode=-100051, errvalue=u"申请资源运行期限不能为空")
    res_unit_fee_empty_err        = error(errcode=-100052, errvalue=u"申请资源费用不能为空")
    res_total_fee_empty_err       = error(errcode=-100053, errvalue=u"申请资源总费用不能为空")
    
    res_computer_invalid_err        = error(errcode=-100060, errvalue=u"申请云主机数据不合法")
    res_cpu_invalid_err             = error(errcode=-100061, errvalue=u"申请CPU数据不合法")
    res_memory_invalid_err          = error(errcode=-100062, errvalue=u"申请内存数据不合法")
    res_disk_invalid_err            = error(errcode=-100063, errvalue=u"申请云磁盘数据不合法")
    res_disk_backup_invalid_err     = error(errcode=-100064, errvalue=u"申请云磁盘备份数据不合法")
    res_out_ip_invalid_err          = error(errcode=-100065, errvalue=u"申请外部IP数据不合法")
    res_snapshot_invalid_err        = error(errcode=-100066, errvalue=u"申请快照数据不合法")
    res_loadbalance_invalid_err     = error(errcode=-100067, errvalue=u"申请应用负载均衡数据不合法")
    res_internet_ip_invalid_err     = error(errcode=-100068, errvalue=u"申请互联网IP数据不合法")
    res_internet_ip_ssl_invalid_err = error(errcode=-100069, errvalue=u"申请是否需要SSL卸载数据不合法")
    res_start_date_invalid_err      = error(errcode=-100070, errvalue=u"申请启动时间数据不合法")
    res_period_invalid_err          = error(errcode=-100071, errvalue=u"申请资源运行期限数据不合法")
    res_unit_fee_invalid_err        = error(errcode=-100072, errvalue=u"申请资源费用数据不合法")
    res_total_fee_invalid_err       = error(errcode=-100073, errvalue=u"申请资源总费用数据不合法")


if __name__ == '__main__':
    print ERROR.username_err.keycode, ERROR.username_err.value
