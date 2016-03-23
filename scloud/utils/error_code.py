# -*- coding: utf-8 -*-

from collections import namedtuple
from tornado.util import ObjectDict
from code import interact

error = namedtuple("operate", ["errvalue", "errcode"])


class ERROR(object):
    system_err = error(errcode=-999999, errvalue=u"系统错误")
    not_found_err = error(errcode=-999404, errvalue=u"对不起！您正在访问的数据资源未找到")
    xsrf_err = error(errcode=-999403, errvalue=u"缺少xsrf参数，禁止提交表单")
    # 注册和登录
    username_empty_err      = error(errcode=-100001, errvalue=u"用户名不能为空")
    username_duplicate_err  = error(errcode=-100017, errvalue=u"该用户名已经被使用")
    username_err            = error(errcode=-100002, errvalue=u"该用户名不存在")
    password_empty_err      = error(errcode=-100003, errvalue=u"密码不能为空")
    password_err            = error(errcode=-100004, errvalue=u"密码错误")
    email_empty_err         = error(errcode=-100005, errvalue=u"邮箱不能为空")
    email_format_err        = error(errcode=-100015, errvalue=u"邮箱格式错误")
    email_duplicate_err     = error(errcode=-100016, errvalue=u"该邮箱已经被使用")
    email_err               = error(errcode=-100006, errvalue=u"邮箱错误")
    mobile_empty_err        = error(errcode=-100007, errvalue=u"手机号不能为空")
    mobile_duplicate_err    = error(errcode=-100018, errvalue=u"该手机号已经被使用")
    mobile_err              = error(errcode=-100008, errvalue=u"手机号错误")
    user_empty_err          = error(errcode=-100009, errvalue=u"操作用户不能为空")
    checker_empty_err       = error(errcode=-100010, errvalue=u"审核用户不能为空")
    old_password_empty_err  = error(errcode=-100011, errvalue=u"旧密码不能为空")
    new_password_empty_err  = error(errcode=-100012, errvalue=u"新密码不能为空")
    repeat_password_empty_err = error(errcode=-100013, errvalue=u"重复密码不能为空")
    repeat_password_err     = error(errcode=-100014, errvalue=u"重复密码与新密码不一致")


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

    res_do_resource_action_err = error(errcode=-100100, errvalue=u"资源审核操作参数有误")
    res_new_apply_err = error(errcode=-100101, errvalue=u"当前状态不允许申请新的资源配额")
    res_revoke_err = error(errcode=-100102, errvalue=u"当前状态不允许资源撤销")
    res_delete_err = error(errcode=-100103, errvalue=u"当前状态不允许资源删除")
    res_re_apply_err = error(errcode=-100104, errvalue=u"当前状态不允许重复申请资源配额")

    res_check_err = error(errcode=-100105, errvalue=u"当前状态不允许对申请资源配额进行审核")
    res_refuse_err = error(errcode=-100106, errvalue=u"当前状态不允许对申请资源配额进行审核")
    res_pay_err = error(errcode=-100107, errvalue=u"当前状态不允许对申请资源配额进行支付")
    res_confirmpay_err = error(errcode=-100108, errvalue=u"当前状态不允许对申请资源配额进行支付确认")
    res_start_err = error(errcode=-100109, errvalue=u"当前状态不允许对申请资源配额启用")
    res_close_err = error(errcode=-100110, errvalue=u"当前状态不允许对申请资源配额关闭")

    env_name_empty_err = error(errcode=-100120, errvalue=u"环境名称不能为空")
    env_desc_empty_err = error(errcode=-100121, errvalue=u"环境说明不能为空")

    env_internet_ip_name_empty_err = error(errcode=-100140, errvalue=u"互联网IP类型名称不能为空")
    env_internet_ip_name_duplicate_err= error(errcode=-100141, errvalue=u"互联网IP类型名称已经存在，不能重复")
    env_internet_ip_fee_invalid_err= error(errcode=-100142, errvalue=u"费用格式不合法")


ERR = ObjectDict()
for attr in dir(ERROR):
    err = getattr(ERROR, attr)
    if isinstance(err, error):
        setattr(ERR, attr.upper(), err.errcode)
        setattr(ERR, str(err.errcode), err.errvalue)

if __name__ == '__main__':
    interact(local=locals())
    print ERROR.username_err
