/* ------------------ 2016-03-23 ------------------ */
CREATE TABLE `pro_user` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `pro_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属项目',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT '提交状态 0:已提交（受理中），1：已处理（已处理）,-1:已拒绝（已拒绝）',
    `email` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '邮箱',
    `username` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '用户名',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `use_vpn` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT '是否需要开通VPN远程访问',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核者ID',
    `check_time` INT(11) NOT NULL DEFAULT '0' COMMENT '审核时间',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目管理用户表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pro_publish` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `pro_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属项目',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT '提交状态 0:已提交（受理中），1：已处理（已处理）,-1:已拒绝（已拒绝）',
    `domain` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '域名',
    `domain_port` int(11) NOT NULL DEFAULT '80' COMMENT '互联网端口',
    `network_address` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '内网地址',
    `network_port` INT(11) NOT NULL DEFAULT '80' COMMENT '内网端口',
    `use_ssl` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT '是否需要SSL卸载',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核者ID',
    `check_time` INT(11) NOT NULL DEFAULT '0' COMMENT '审核时间',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目互联网发布表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pro_balance` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `pro_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属项目',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT '提交状态 0:已提交（受理中），1：已处理（已处理）,-1:已拒绝（已拒绝）',
    `res_apply_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属资源申请',
    `members` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '成员',
    `plot` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '策略',
    `health` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '策略',
    `url` VARCHAR(255) NOT NULL DEFAULT '' COMMENT 'URL（仅限HTTP方式）',
    `keyword` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '关键字（仅限HTTP方式）',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '特殊说明',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核者ID',
    `check_time` INT(11) NOT NULL DEFAULT '0' COMMENT '审核时间',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目互联网发布表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pro_backup` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `pro_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属项目',
    `res_apply_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属资源申请',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT '提交状态 0:已提交（受理中），1：已处理（已处理）,-1:已拒绝（已拒绝）',
    `plot` VARCHAR(1024) NOT NULL DEFAULT '' COMMENT '策略(json格式)',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核者ID',
    `check_time` INT(11) NOT NULL DEFAULT '0' COMMENT '审核时间',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目资源备份表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;
/* ------------------ 2016-01-20 ------------------ */
CREATE TABLE `pt_user` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `email` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '邮箱',
    `mobile` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '手机号',
    `username` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '用户名',
    `password` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '登录密码',
    `last_login` DATETIME NOT NULL DEFAULT  '0000-00-00 00:00:00' COMMENT '上次登录时间',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='管理员用户表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;


CREATE TABLE `pt_group` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '组名',
    `keyword` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '关键字',
    `keycode` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '关键字代码',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='管理员用户表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;


CREATE TABLE `pt_perm` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '权限名称',
    `keyword` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '关键字',
    `keycode` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '关键字代码',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='管理员用户表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;


CREATE TABLE `pt_group_perms` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `group_id` INT(11) NOT NULL DEFAULT '0' COMMENT '分组ID',
    `perm_id` INT(11) NOT NULL DEFAULT '0' COMMENT '权限ID',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='管理员用户表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pt_role` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '描述名称',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '角色描述',
    `remark` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '注释',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='角色表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pt_role_group_ops` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `role_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `group_keycode` INT(11) NOT NULL DEFAULT '0' COMMENT '分组关键编码',
    `op_keycode` INT(11) NOT NULL DEFAULT '0' COMMENT '操作关键编码',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='角色权限表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pt_role_groups` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `role_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `group_perm_id` INT(11) NOT NULL DEFAULT '0' COMMENT '分组ID',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='角色权限表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pt_user_role` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `role_id` INT(11) NOT NULL DEFAULT '0' COMMENT '角色ID',
    `is_enable` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '是否可用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='角色权限表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;
/* ------------------ 2016-01-18 ------------------ */
CREATE TABLE `pro_info` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '项目名称',
    `owner` VARCHAR(255) NOT NULL DEFAULT '0' COMMENT '项目负责人',
    `owner_mobile` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '项目负责人',
    `owner_email` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '项目负责人',
    `env_id` INT(11) NOT NULL DEFAULT '0' COMMENT '环境ID',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '项目描述',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核者ID',
    `check_time` INT(11) NOT NULL DEFAULT '0' COMMENT '审核时间',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `env_info` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '环境名称',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '环境描述',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目环境表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `pro_resource_apply` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `pro_id` INT(11) NOT NULL DEFAULT '0' COMMENT '所属项目',
    `computer` INT(11) NOT NULL DEFAULT '0' COMMENT '云主机数量',
    `cpu` INT(11) NOT NULL DEFAULT '0' COMMENT 'CPU数量',
    `memory` INT(11) NOT NULL DEFAULT '0' COMMENT '内存数量',
    `disk` INT(11) NOT NULL DEFAULT '0' COMMENT '云磁盘数量',
    `disk_backup` INT(11) NOT NULL DEFAULT '0' COMMENT '云磁盘备份数量',
    `out_ip` INT(11) NOT NULL DEFAULT '0' COMMENT '外部IP数量',
    `snapshot` INT(11) NOT NULL DEFAULT '0' COMMENT '快照数量',
    `loadbalance` INT(11) NOT NULL DEFAULT '0' COMMENT '应用负载均衡数量',
    `internet_ip` INT(11) NOT NULL DEFAULT '-1' COMMENT '互联网IP',
    `internet_ip_ssl` INT(11) NOT NULL DEFAULT '-1' COMMENT '互联网IP是否需要SSL卸载',
    `desc` VARCHAR(512) NOT NULL DEFAULT '创建项目' COMMENT '变更描述',
    `start_date` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '启动时间',
    `period` INT(11) NOT NULL DEFAULT '0' COMMENT '运行期（月）',
    `due_date` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '到期时间',
    `unit_fee` float(11,4) NOT NULL DEFAULT '0.00' COMMENT '本月费用',
    `total_fee` float(11,4) NOT NULL DEFAULT '0.00' COMMENT '合计费用',
    `fee_desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '费用产生描述（计算结果给出）',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT '资源申请状态 0:提交（待审核），1：已审核（待支付），2已支付（完成）',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '申请人',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核人',
    `check_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '审核时间',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='项目资源申请表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `env_resource_fee` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `env_id` INT(11) NOT NULL DEFAULT '0' COMMENT '项目环境ID',
    `computer` INT(11) NOT NULL DEFAULT '0' COMMENT '云主机单价费用',
    `cpu` INT(11) NOT NULL DEFAULT '0' COMMENT 'CPU单价费用',
    `memory` INT(11) NOT NULL DEFAULT '0' COMMENT '内存单价费用',
    `disk` INT(11) NOT NULL DEFAULT '0' COMMENT '云磁盘单价费用',
    `disk_backup` INT(11) NOT NULL DEFAULT '0' COMMENT '云磁盘备份单价费用',
    `out_ip` INT(11) NOT NULL DEFAULT '0' COMMENT '外部IP单价费用',
    `snapshot` INT(11) NOT NULL DEFAULT '0' COMMENT '快照单价费用',
    `loadbalance` INT(11) NOT NULL DEFAULT '0' COMMENT '应用负载均衡单价费用',
    `internet_ip` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '互联网IP类型费用（JSON）',
    `internet_ip_ssl` INT(11) NOT NULL DEFAULT '0' COMMENT '互联网IP是否需要SSL卸载',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `env_id` (`env_id`),
    CONSTRAINT `env_resource_fee_ibfk_1` FOREIGN KEY (`env_id`) REFERENCES `env_info` (`id`) ON DELETE CASCADE
)
COMMENT='环境资源单价费用表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `env_resource_value` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `env_id` INT(11) NOT NULL DEFAULT '0' COMMENT '项目环境ID',
    `computer` INT(11) NOT NULL DEFAULT '0' COMMENT '云主机默认推荐值',
    `cpu` INT(11) NOT NULL DEFAULT '0' COMMENT 'CPU默认推荐值',
    `memory` INT(11) NOT NULL DEFAULT '0' COMMENT '内存默认推荐值',
    `disk` INT(11) NOT NULL DEFAULT '0' COMMENT '云磁盘默认推荐值',
    `disk_backup` INT(11) NOT NULL DEFAULT '0' COMMENT '云磁盘备份默认推荐值',
    `out_ip` INT(11) NOT NULL DEFAULT '0' COMMENT '外部IP默认推荐值',
    `snapshot` INT(11) NOT NULL DEFAULT '0' COMMENT '快照默认推荐值',
    `loadbalance` INT(11) NOT NULL DEFAULT '0' COMMENT '应用负载均衡默认推荐值',
    `internet_ip` INT(11) NOT NULL DEFAULT '0' COMMENT '互联网IP类型默认推荐值',
    `internet_ip_ssl` INT(11) NOT NULL DEFAULT '0' COMMENT '互联网IP是否需要SSL卸载默认推荐值',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `env_id` (`env_id`),
    CONSTRAINT `env_resource_value_ibfk_1` FOREIGN KEY (`env_id`) REFERENCES `env_info` (`id`) ON DELETE CASCADE
)
COMMENT='环境资源默认值表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `env_internet_ip_types` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `env_id` INT(11) NOT NULL DEFAULT '0' COMMENT '项目环境ID',
    `name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '外网IP分类名称',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '外网IP分类描述',
    `fee` float(11,2) NOT NULL DEFAULT '0.00' COMMENT '相关费用',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    KEY `env_id` (`env_id`),
    CONSTRAINT `env_internet_ip_types_ibfk_1` FOREIGN KEY (`env_id`) REFERENCES `env_info` (`id`) ON DELETE CASCADE
)
COMMENT='环境外网IP分类表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `act_history` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `record_id` INT(11) NOT NULL DEFAULT '0' COMMENT '数据编码',
    `record_table` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '数据表名',
    `act_type` INT(11) NOT NULL DEFAULT '0' COMMENT '数据库操作类型 1：添加，2：修改，3：删除，9：其他',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '数据库操作描述',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '数据库操作人员',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='数据库操作历史表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `act_pro_history` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `pro_id` INT(11) NOT NULL DEFAULT '0' COMMENT '项目ID',
    `res_apply_id` INT(11) NOT NULL DEFAULT '0' COMMENT '资源申请ID',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT '项目申请状态',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '数据库操作描述',
    `user_id` INT(11) NOT NULL DEFAULT '0' COMMENT '数据库操作人员',
    `checker_id` INT(11) NOT NULL DEFAULT '0' COMMENT '审核人员',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='数据库操作历史表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;

CREATE TABLE `act_todo` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `important` INT(11) NOT NULL DEFAULT '0' COMMENT 'TODO操作紧急程度',
    `desc` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '数据库操作描述',
    `from_user_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'TODO操作发起人',
    `to_user_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'TODO操作人',
    `status` INT(11) NOT NULL DEFAULT '0' COMMENT 'TODO事件状态 0：新创建，1：进行中，9：已完成',
    `create_time` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
    `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='TODO信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=0;
