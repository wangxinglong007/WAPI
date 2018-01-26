/*
Navicat MySQL Data Transfer

Source Server         : APIAutoTest
Source Server Version : 50623
Source Host           : xxx6
Source Database       : test_django

Target Server Type    : MYSQL
Target Server Version : 50623
File Encoding         : 65001

Date: 2018-01-26 13:58:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `name` (`name`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=5

;

-- ----------------------------
-- Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`group_id`  int(11) NOT NULL ,
`permission_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`, `permission_id`) USING BTREE ,
INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=444

;

-- ----------------------------
-- Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`content_type_id`  int(11) NOT NULL ,
`codename`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`, `codename`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=244

;

-- ----------------------------
-- Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`password`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`last_login`  datetime(6) NULL DEFAULT NULL ,
`is_superuser`  tinyint(1) NOT NULL ,
`username`  varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`first_name`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`last_name`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`email`  varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`is_staff`  tinyint(1) NOT NULL ,
`is_active`  tinyint(1) NOT NULL ,
`date_joined`  datetime(6) NOT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `username` (`username`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=35

;

-- ----------------------------
-- Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`user_id`  int(11) NOT NULL ,
`group_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`, `group_id`) USING BTREE ,
INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=19

;

-- ----------------------------
-- Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`user_id`  int(11) NOT NULL ,
`permission_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`, `permission_id`) USING BTREE ,
INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=25

;

-- ----------------------------
-- Table structure for `celery_taskmeta`
-- ----------------------------
DROP TABLE IF EXISTS `celery_taskmeta`;
CREATE TABLE `celery_taskmeta` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`task_id`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`status`  varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`result`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`date_done`  datetime(6) NOT NULL ,
`traceback`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`hidden`  tinyint(1) NOT NULL ,
`meta`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `task_id` (`task_id`) USING BTREE ,
INDEX `celery_taskmeta_hidden_23fd02dc` (`hidden`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Table structure for `celery_tasksetmeta`
-- ----------------------------
DROP TABLE IF EXISTS `celery_tasksetmeta`;
CREATE TABLE `celery_tasksetmeta` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`taskset_id`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`result`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`date_done`  datetime(6) NOT NULL ,
`hidden`  tinyint(1) NOT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `taskset_id` (`taskset_id`) USING BTREE ,
INDEX `celery_tasksetmeta_hidden_593cfc24` (`hidden`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`action_time`  datetime(6) NOT NULL ,
`object_id`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`object_repr`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`action_flag`  smallint(5) UNSIGNED NOT NULL ,
`change_message`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`content_type_id`  int(11) NULL DEFAULT NULL ,
`user_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`) USING BTREE ,
INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=8103

;

-- ----------------------------
-- Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`app_label`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`model`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`, `model`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=82

;

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`app`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`name`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`applied`  datetime(6) NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=94

;

-- ----------------------------
-- Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
`session_key`  varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`session_data`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`expire_date`  datetime(6) NOT NULL ,
PRIMARY KEY (`session_key`),
INDEX `django_session_expire_date_a5c62663` (`expire_date`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `djcelery_crontabschedule`
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_crontabschedule`;
CREATE TABLE `djcelery_crontabschedule` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`minute`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`hour`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`day_of_week`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`day_of_month`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`month_of_year`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=16

;

-- ----------------------------
-- Table structure for `djcelery_intervalschedule`
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_intervalschedule`;
CREATE TABLE `djcelery_intervalschedule` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`every`  int(11) NOT NULL ,
`period`  varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=12

;

-- ----------------------------
-- Table structure for `djcelery_periodictask`
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_periodictask`;
CREATE TABLE `djcelery_periodictask` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`task`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`args`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`kwargs`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`queue`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`exchange`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`routing_key`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`expires`  datetime(6) NULL DEFAULT NULL ,
`enabled`  tinyint(1) NOT NULL ,
`last_run_at`  datetime(6) NULL DEFAULT NULL ,
`total_run_count`  int(10) UNSIGNED NOT NULL ,
`date_changed`  datetime(6) NOT NULL ,
`description`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`crontab_id`  int(11) NULL DEFAULT NULL ,
`interval_id`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `name` (`name`) USING BTREE ,
INDEX `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` (`crontab_id`) USING BTREE ,
INDEX `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` (`interval_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=37

;

-- ----------------------------
-- Table structure for `djcelery_periodictasks`
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_periodictasks`;
CREATE TABLE `djcelery_periodictasks` (
`ident`  smallint(6) NOT NULL ,
`last_update`  datetime(6) NOT NULL ,
PRIMARY KEY (`ident`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `djcelery_taskstate`
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_taskstate`;
CREATE TABLE `djcelery_taskstate` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`state`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`task_id`  varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`name`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`tstamp`  datetime(6) NOT NULL ,
`args`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`kwargs`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`eta`  datetime(6) NULL DEFAULT NULL ,
`expires`  datetime(6) NULL DEFAULT NULL ,
`result`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`traceback`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`runtime`  double NULL DEFAULT NULL ,
`retries`  int(11) NOT NULL ,
`hidden`  tinyint(1) NOT NULL ,
`worker_id`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `task_id` (`task_id`) USING BTREE ,
INDEX `djcelery_taskstate_state_53543be4` (`state`) USING BTREE ,
INDEX `djcelery_taskstate_name_8af9eded` (`name`) USING BTREE ,
INDEX `djcelery_taskstate_tstamp_4c3f93a1` (`tstamp`) USING BTREE ,
INDEX `djcelery_taskstate_hidden_c3905e57` (`hidden`) USING BTREE ,
INDEX `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` (`worker_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Table structure for `djcelery_workerstate`
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_workerstate`;
CREATE TABLE `djcelery_workerstate` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`hostname`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`last_heartbeat`  datetime(6) NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `hostname` (`hostname`) USING BTREE ,
INDEX `djcelery_workerstate_last_heartbeat_4539b544` (`last_heartbeat`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1

;

-- ----------------------------
-- Table structure for `djkombu_message`
-- ----------------------------
DROP TABLE IF EXISTS `djkombu_message`;
CREATE TABLE `djkombu_message` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`visible`  tinyint(1) NOT NULL ,
`sent_at`  datetime(6) NULL DEFAULT NULL ,
`payload`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`queue_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`queue_id`) REFERENCES `djkombu_queue` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `djkombu_message_visible_3ca5f33e` (`visible`) USING BTREE ,
INDEX `djkombu_message_sent_at_680ecd55` (`sent_at`) USING BTREE ,
INDEX `djkombu_message_queue_id_38d205a7_fk_djkombu_queue_id` (`queue_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=4443

;

-- ----------------------------
-- Table structure for `djkombu_queue`
-- ----------------------------
DROP TABLE IF EXISTS `djkombu_queue`;
CREATE TABLE `djkombu_queue` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `name` (`name`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=68

;

-- ----------------------------
-- Table structure for `pbd_dym_subtestcase`
-- ----------------------------
DROP TABLE IF EXISTS `pbd_dym_subtestcase`;
CREATE TABLE `pbd_dym_subtestcase` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SetupIndex`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'setup执行顺序' ,
`CaseID`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '主表测试用例的ID' ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '接口uri' ,
`Description`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述' ,
`UrlParameter`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'uri参数' ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '请求方法get/post' ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '信息头' ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'body值' ,
`DataBox`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '预期的的字段路径和值' ,
`APIResult`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '返回结果' ,
`SetupType`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '初始化类型 api/sql' ,
`UpdateTime`  datetime(6) NULL DEFAULT NULL COMMENT '用例更新时间' ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=22

;

-- ----------------------------
-- Table structure for `pbd_dym_testcase`
-- ----------------------------
DROP TABLE IF EXISTS `pbd_dym_testcase`;
CREATE TABLE `pbd_dym_testcase` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`TestCaseDescription`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`SetupStep`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`UrlParameter`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`Expect`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`APIResult`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`UpdateTime`  datetime(6) NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=3

;

-- ----------------------------
-- Table structure for `pbs_dy_testcase`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dy_testcase`;
CREATE TABLE `pbs_dy_testcase` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`TestCaseDescription`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`SetupStep`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`UrlParameter`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Expect`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`APIResult`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`UpdateTime`  datetime(6) NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=2

;

-- ----------------------------
-- Table structure for `pbs_dynamic_abs`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_abs`;
CREATE TABLE `pbs_dynamic_abs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=22

;

-- ----------------------------
-- Table structure for `pbs_dynamic_absbusiness`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_absbusiness`;
CREATE TABLE `pbs_dynamic_absbusiness` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=3

;

-- ----------------------------
-- Table structure for `pbs_dynamic_absbusinesspbs`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_absbusinesspbs`;
CREATE TABLE `pbs_dynamic_absbusinesspbs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=5

;

-- ----------------------------
-- Table structure for `pbs_dynamic_absforpbs`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_absforpbs`;
CREATE TABLE `pbs_dynamic_absforpbs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=6

;

-- ----------------------------
-- Table structure for `pbs_dynamic_absonline`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_absonline`;
CREATE TABLE `pbs_dynamic_absonline` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=13

;

-- ----------------------------
-- Table structure for `pbs_dynamic_absticketservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_absticketservice`;
CREATE TABLE `pbs_dynamic_absticketservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=20

;

-- ----------------------------
-- Table structure for `pbs_dynamic_accountservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_accountservice`;
CREATE TABLE `pbs_dynamic_accountservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=16

;

-- ----------------------------
-- Table structure for `pbs_dynamic_accountwebapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_accountwebapi`;
CREATE TABLE `pbs_dynamic_accountwebapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=125

;

-- ----------------------------
-- Table structure for `pbs_dynamic_cbs`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_cbs`;
CREATE TABLE `pbs_dynamic_cbs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=37

;

-- ----------------------------
-- Table structure for `pbs_dynamic_cbsweb`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_cbsweb`;
CREATE TABLE `pbs_dynamic_cbsweb` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=50

;

-- ----------------------------
-- Table structure for `pbs_dynamic_cmsservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_cmsservice`;
CREATE TABLE `pbs_dynamic_cmsservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=2

;

-- ----------------------------
-- Table structure for `pbs_dynamic_crm`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_crm`;
CREATE TABLE `pbs_dynamic_crm` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=94

;

-- ----------------------------
-- Table structure for `pbs_dynamic_crmbusinessapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_crmbusinessapi`;
CREATE TABLE `pbs_dynamic_crmbusinessapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=338

;

-- ----------------------------
-- Table structure for `pbs_dynamic_crmservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_crmservice`;
CREATE TABLE `pbs_dynamic_crmservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=7

;

-- ----------------------------
-- Table structure for `pbs_dynamic_fbsferry`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_fbsferry`;
CREATE TABLE `pbs_dynamic_fbsferry` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=33

;

-- ----------------------------
-- Table structure for `pbs_dynamic_fbsferryforcbs`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_fbsferryforcbs`;
CREATE TABLE `pbs_dynamic_fbsferryforcbs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=18

;

-- ----------------------------
-- Table structure for `pbs_dynamic_ferryservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_ferryservice`;
CREATE TABLE `pbs_dynamic_ferryservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=27

;

-- ----------------------------
-- Table structure for `pbs_dynamic_flightservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_flightservice`;
CREATE TABLE `pbs_dynamic_flightservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=14

;

-- ----------------------------
-- Table structure for `pbs_dynamic_hotelservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_hotelservice`;
CREATE TABLE `pbs_dynamic_hotelservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=13

;

-- ----------------------------
-- Table structure for `pbs_dynamic_ignite`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_ignite`;
CREATE TABLE `pbs_dynamic_ignite` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`Name`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`Host_id`) REFERENCES `pbs_dynamic_systemhost` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `PBS_Dynamic_ignite_Host_id_dc570bd8_fk_PBS_Dynamic_systemhost_id` (`Host_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=44

;

-- ----------------------------
-- Table structure for `pbs_dynamic_infrastructureservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_infrastructureservice`;
CREATE TABLE `pbs_dynamic_infrastructureservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=6

;

-- ----------------------------
-- Table structure for `pbs_dynamic_lbsapp`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_lbsapp`;
CREATE TABLE `pbs_dynamic_lbsapp` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=21

;

-- ----------------------------
-- Table structure for `pbs_dynamic_lbsbooking`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_lbsbooking`;
CREATE TABLE `pbs_dynamic_lbsbooking` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=59

;

-- ----------------------------
-- Table structure for `pbs_dynamic_lbsproduct`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_lbsproduct`;
CREATE TABLE `pbs_dynamic_lbsproduct` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=116

;

-- ----------------------------
-- Table structure for `pbs_dynamic_marketrestapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_marketrestapi`;
CREATE TABLE `pbs_dynamic_marketrestapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=20

;

-- ----------------------------
-- Table structure for `pbs_dynamic_motorestapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_motorestapi`;
CREATE TABLE `pbs_dynamic_motorestapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL COMMENT '0执行 1不执行 2需要传body' ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=61

;

-- ----------------------------
-- Table structure for `pbs_dynamic_motoservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_motoservice`;
CREATE TABLE `pbs_dynamic_motoservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=3

;

-- ----------------------------
-- Table structure for `pbs_dynamic_motowebapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_motowebapi`;
CREATE TABLE `pbs_dynamic_motowebapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=10

;

-- ----------------------------
-- Table structure for `pbs_dynamic_packagecbservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_packagecbservice`;
CREATE TABLE `pbs_dynamic_packagecbservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=5

;

-- ----------------------------
-- Table structure for `pbs_dynamic_packagefhservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_packagefhservice`;
CREATE TABLE `pbs_dynamic_packagefhservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=28

;

-- ----------------------------
-- Table structure for `pbs_dynamic_packageservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_packageservice`;
CREATE TABLE `pbs_dynamic_packageservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=14

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbsdynamich5`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbsdynamich5`;
CREATE TABLE `pbs_dynamic_pbsdynamich5` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=50

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbsh5static`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbsh5static`;
CREATE TABLE `pbs_dynamic_pbsh5static` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=53

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbsh5staticl`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbsh5staticl`;
CREATE TABLE `pbs_dynamic_pbsh5staticl` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=55

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbsservice`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbsservice`;
CREATE TABLE `pbs_dynamic_pbsservice` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=6

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbswebdynamic`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbswebdynamic`;
CREATE TABLE `pbs_dynamic_pbswebdynamic` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=123

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbswebstatic`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbswebstatic`;
CREATE TABLE `pbs_dynamic_pbswebstatic` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=105

;

-- ----------------------------
-- Table structure for `pbs_dynamic_pbswebstaticl`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_pbswebstaticl`;
CREATE TABLE `pbs_dynamic_pbswebstaticl` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=97

;

-- ----------------------------
-- Table structure for `pbs_dynamic_rbs`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_rbs`;
CREATE TABLE `pbs_dynamic_rbs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=19

;

-- ----------------------------
-- Table structure for `pbs_dynamic_report`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_report`;
CREATE TABLE `pbs_dynamic_report` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`CaseID`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ClickExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`testCase_id`  int(11) NULL DEFAULT NULL ,
`Environment`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`),
INDEX `PBS_Dynamic_report_CaseID_1e76bef1` (`CaseID`) USING BTREE ,
INDEX `PBS_Dynamic_report_ClickExecutionTime` (`ClickExecutionTime`) USING BTREE ,
INDEX `PBS_Dynamic_report_Environment` (`Environment`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=744596

;

-- ----------------------------
-- Table structure for `pbs_dynamic_rmwebapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_rmwebapi`;
CREATE TABLE `pbs_dynamic_rmwebapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=57

;

-- ----------------------------
-- Table structure for `pbs_dynamic_statistics`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_statistics`;
CREATE TABLE `pbs_dynamic_statistics` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`success`  int(11) NULL DEFAULT NULL ,
`fail`  int(11) NULL DEFAULT NULL ,
`error`  int(11) NULL DEFAULT NULL ,
`total`  int(11) NULL DEFAULT NULL ,
`statistics_time`  datetime(6) NULL DEFAULT NULL ,
`chart_type`  int(11) NULL DEFAULT NULL ,
`interface_name`  varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`api_name_id`  int(11) NULL DEFAULT NULL ,
`statistics_id`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`api_name_id`) REFERENCES `pbs_dynamic_testcase` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`statistics_id`) REFERENCES `pbs_dynamic_systemhost` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `PBS_Dynamic_statisti_api_name_id_94a392ed_fk_PBS_Dynam` (`api_name_id`) USING BTREE ,
INDEX `PBS_Dynamic_statisti_statistics_id_a2eddbae_fk_PBS_Dynam` (`statistics_id`) USING BTREE ,
INDEX `PBS_Dynamic_statistics_statistics_time_043f06cb` (`statistics_time`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=31881

;

-- ----------------------------
-- Table structure for `pbs_dynamic_subreport`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_subreport`;
CREATE TABLE `pbs_dynamic_subreport` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`ClickExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`SubCaseID_id`  int(11) NOT NULL ,
`CaseID`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Environment`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`SubCaseID_id`) REFERENCES `pbs_dynamic_subtestcase` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `PBS_Dynamic_subreport_SubCaseID_id_2adf6cbb` (`SubCaseID_id`) USING BTREE ,
INDEX `PBS_Dynamic_subreport_CaseID` (`CaseID`) USING BTREE ,
INDEX `PBS_Dynamic_report_ClickExecutionTime` (`ClickExecutionTime`) USING BTREE ,
INDEX `PBS_Dynamic_subreport_Environment` (`Environment`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=1576359

;

-- ----------------------------
-- Table structure for `pbs_dynamic_subtestcase`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_subtestcase`;
CREATE TABLE `pbs_dynamic_subtestcase` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SetupIndex`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`CaseID`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`UrlParameter`  varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`DataBox`  varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`SetupType`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'API' ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Host`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=498

;

-- ----------------------------
-- Table structure for `pbs_dynamic_subtestcase20180108`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_subtestcase20180108`;
CREATE TABLE `pbs_dynamic_subtestcase20180108` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SetupIndex`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`CaseID`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`UrlParameter`  varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`DataBox`  varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`SetupType`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'API' ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Host`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=498

;

-- ----------------------------
-- Table structure for `pbs_dynamic_systemhost`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_systemhost`;
CREATE TABLE `pbs_dynamic_systemhost` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Environment`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Uri`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`SystemType`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=153

;

-- ----------------------------
-- Table structure for `pbs_dynamic_systemhost20180108`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_systemhost20180108`;
CREATE TABLE `pbs_dynamic_systemhost20180108` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Environment`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Uri`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`SystemType`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=153

;

-- ----------------------------
-- Table structure for `pbs_dynamic_tbsapp`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_tbsapp`;
CREATE TABLE `pbs_dynamic_tbsapp` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=43

;

-- ----------------------------
-- Table structure for `pbs_dynamic_tbsbookingapi`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_tbsbookingapi`;
CREATE TABLE `pbs_dynamic_tbsbookingapi` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=170

;

-- ----------------------------
-- Table structure for `pbs_dynamic_tbsweb`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_tbsweb`;
CREATE TABLE `pbs_dynamic_tbsweb` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`SystemType`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecuteStatus`  int(11) NOT NULL ,
`Parameter`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=86

;

-- ----------------------------
-- Table structure for `pbs_dynamic_template`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_template`;
CREATE TABLE `pbs_dynamic_template` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Content`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`Host`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=57

;

-- ----------------------------
-- Table structure for `pbs_dynamic_template_copy`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_template_copy`;
CREATE TABLE `pbs_dynamic_template_copy` (
`ID`  int(11) NOT NULL ,
`ApiName`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Content`  mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
PRIMARY KEY (`ID`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `pbs_dynamic_testcase`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_testcase`;
CREATE TABLE `pbs_dynamic_testcase` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`SetupStep`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' ,
`UrlParameter`  varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Expect`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`User`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Editor`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
INDEX `PBS_Dynamic_testcase_Host_id_fk_PBS_Dynam` (`Host_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=2256

;

-- ----------------------------
-- Table structure for `pbs_dynamic_testcase_suite_1101`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_testcase_suite_1101`;
CREATE TABLE `pbs_dynamic_testcase_suite_1101` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`testcase_id`  int(11) NOT NULL ,
`testsuite_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`testcase_id`) REFERENCES `pbs_dynamic_testcase` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`testsuite_id`) REFERENCES `pbs_dynamic_testsuite` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `PBS_Dynamic_testcase_Sui_testcase_id_testsuite_id_bb5837b8_uniq` (`testcase_id`, `testsuite_id`) USING BTREE ,
INDEX `PBS_Dynamic_testcase_testsuite_id_b1a79c15_fk_PBS_Dynam` (`testsuite_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=2680

;

-- ----------------------------
-- Table structure for `pbs_dynamic_testcase20180108`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_testcase20180108`;
CREATE TABLE `pbs_dynamic_testcase20180108` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`ApiName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`SetupStep`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' ,
`UrlParameter`  varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Method`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`Expect`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`Status`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`HostName`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`User`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Editor`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
INDEX `PBS_Dynamic_testcase_Host_id_fk_PBS_Dynam` (`Host_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=2256

;

-- ----------------------------
-- Table structure for `pbs_dynamic_testsuite`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_testsuite`;
CREATE TABLE `pbs_dynamic_testsuite` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`Name`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Description`  varchar(4096) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`User`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Email`  tinyint(1) NOT NULL ,
`Pattern`  tinyint(1) NOT NULL ,
`ApiType`  varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=59

;

-- ----------------------------
-- Table structure for `pbs_dynamic_testsuite20180108`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_testsuite20180108`;
CREATE TABLE `pbs_dynamic_testsuite20180108` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`Name`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Description`  varchar(4096) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`User`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`Email`  tinyint(1) NOT NULL ,
`Pattern`  tinyint(1) NOT NULL ,
`ApiType`  varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=59

;

-- ----------------------------
-- Table structure for `pbs_dynamic_updatehost`
-- ----------------------------
DROP TABLE IF EXISTS `pbs_dynamic_updatehost`;
CREATE TABLE `pbs_dynamic_updatehost` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`EnvironmentName`  varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Content`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=2

;

-- ----------------------------
-- Table structure for `soap_api_soapreport`
-- ----------------------------
DROP TABLE IF EXISTS `soap_api_soapreport`;
CREATE TABLE `soap_api_soapreport` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`CaseID`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`ClickExecutionTime`  datetime(6) NOT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`Environment`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`soapTestCase_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`soapTestCase_id`) REFERENCES `soap_api_soaptestcases` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `SOAP_API_soapreport_soapTestCase_id_0e6a4b85_fk_SOAP_API_` (`soapTestCase_id`) USING BTREE ,
INDEX `SOAP_API_soapreport_CaseID_800351f1` (`CaseID`) USING BTREE ,
INDEX `SOAP_API_soapreport_ClickExecutionTime_3f810506` (`ClickExecutionTime`) USING BTREE ,
INDEX `SOAP_API_soapreport_Environment_9844bc27` (`Environment`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=45

;

-- ----------------------------
-- Table structure for `soap_api_soapsubreport`
-- ----------------------------
DROP TABLE IF EXISTS `soap_api_soapsubreport`;
CREATE TABLE `soap_api_soapsubreport` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`CaseID`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`ClickExecutionTime`  datetime(6) NOT NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`Environment`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`soapSubCase_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`soapSubCase_id`) REFERENCES `soap_api_soapsubtestcases` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `SOAP_API_soapsubrepo_soapSubCase_id_ee6dc960_fk_SOAP_API_` (`soapSubCase_id`) USING BTREE ,
INDEX `SOAP_API_soapsubreport_CaseID_c814057e` (`CaseID`) USING BTREE ,
INDEX `SOAP_API_soapsubreport_ClickExecutionTime_25d5c7d2` (`ClickExecutionTime`) USING BTREE ,
INDEX `SOAP_API_soapsubreport_Environment_7b4d45a3` (`Environment`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=45

;

-- ----------------------------
-- Table structure for `soap_api_soapsubtestcases`
-- ----------------------------
DROP TABLE IF EXISTS `soap_api_soapsubtestcases`;
CREATE TABLE `soap_api_soapsubtestcases` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`HostName`  varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`SetupType`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`SetupIndex`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`CaseID`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`DataBox`  varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`Host_id`) REFERENCES `pbs_dynamic_systemhost` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `SOAP_API_soapsubtest_Host_id_08f0fc9c_fk_PBS_Dynam` (`Host_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=2

;

-- ----------------------------
-- Table structure for `soap_api_soaptestcases`
-- ----------------------------
DROP TABLE IF EXISTS `soap_api_soaptestcases`;
CREATE TABLE `soap_api_soaptestcases` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`HostName`  varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Description`  varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Method`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Headers`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`BodyValues`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`APIResult`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL ,
`ExecutionTime`  datetime(6) NULL DEFAULT NULL ,
`CreateTime`  datetime(6) NULL DEFAULT NULL ,
`UseTime`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`SetupStep`  varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Expect`  varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL ,
`Status`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`User`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`Editor`  varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL ,
`Host_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`Host_id`) REFERENCES `pbs_dynamic_systemhost` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `SOAP_API_soaptestcas_Host_id_6cbca875_fk_PBS_Dynam` (`Host_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
AUTO_INCREMENT=4

;

-- ----------------------------
-- Auto increment value for `auth_group`
-- ----------------------------
ALTER TABLE `auth_group` AUTO_INCREMENT=5;

-- ----------------------------
-- Auto increment value for `auth_group_permissions`
-- ----------------------------
ALTER TABLE `auth_group_permissions` AUTO_INCREMENT=444;

-- ----------------------------
-- Auto increment value for `auth_permission`
-- ----------------------------
ALTER TABLE `auth_permission` AUTO_INCREMENT=244;

-- ----------------------------
-- Auto increment value for `auth_user`
-- ----------------------------
ALTER TABLE `auth_user` AUTO_INCREMENT=35;

-- ----------------------------
-- Auto increment value for `auth_user_groups`
-- ----------------------------
ALTER TABLE `auth_user_groups` AUTO_INCREMENT=19;

-- ----------------------------
-- Auto increment value for `auth_user_user_permissions`
-- ----------------------------
ALTER TABLE `auth_user_user_permissions` AUTO_INCREMENT=25;

-- ----------------------------
-- Auto increment value for `celery_taskmeta`
-- ----------------------------
ALTER TABLE `celery_taskmeta` AUTO_INCREMENT=1;

-- ----------------------------
-- Auto increment value for `celery_tasksetmeta`
-- ----------------------------
ALTER TABLE `celery_tasksetmeta` AUTO_INCREMENT=1;

-- ----------------------------
-- Auto increment value for `django_admin_log`
-- ----------------------------
ALTER TABLE `django_admin_log` AUTO_INCREMENT=8103;

-- ----------------------------
-- Auto increment value for `django_content_type`
-- ----------------------------
ALTER TABLE `django_content_type` AUTO_INCREMENT=82;

-- ----------------------------
-- Auto increment value for `django_migrations`
-- ----------------------------
ALTER TABLE `django_migrations` AUTO_INCREMENT=94;

-- ----------------------------
-- Auto increment value for `djcelery_crontabschedule`
-- ----------------------------
ALTER TABLE `djcelery_crontabschedule` AUTO_INCREMENT=16;

-- ----------------------------
-- Auto increment value for `djcelery_intervalschedule`
-- ----------------------------
ALTER TABLE `djcelery_intervalschedule` AUTO_INCREMENT=12;

-- ----------------------------
-- Auto increment value for `djcelery_periodictask`
-- ----------------------------
ALTER TABLE `djcelery_periodictask` AUTO_INCREMENT=37;

-- ----------------------------
-- Auto increment value for `djcelery_taskstate`
-- ----------------------------
ALTER TABLE `djcelery_taskstate` AUTO_INCREMENT=1;

-- ----------------------------
-- Auto increment value for `djcelery_workerstate`
-- ----------------------------
ALTER TABLE `djcelery_workerstate` AUTO_INCREMENT=1;

-- ----------------------------
-- Auto increment value for `djkombu_message`
-- ----------------------------
ALTER TABLE `djkombu_message` AUTO_INCREMENT=4443;

-- ----------------------------
-- Auto increment value for `djkombu_queue`
-- ----------------------------
ALTER TABLE `djkombu_queue` AUTO_INCREMENT=68;

-- ----------------------------
-- Auto increment value for `pbd_dym_subtestcase`
-- ----------------------------
ALTER TABLE `pbd_dym_subtestcase` AUTO_INCREMENT=22;

-- ----------------------------
-- Auto increment value for `pbd_dym_testcase`
-- ----------------------------
ALTER TABLE `pbd_dym_testcase` AUTO_INCREMENT=3;

-- ----------------------------
-- Auto increment value for `pbs_dy_testcase`
-- ----------------------------
ALTER TABLE `pbs_dy_testcase` AUTO_INCREMENT=2;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_abs`
-- ----------------------------
ALTER TABLE `pbs_dynamic_abs` AUTO_INCREMENT=22;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_absbusiness`
-- ----------------------------
ALTER TABLE `pbs_dynamic_absbusiness` AUTO_INCREMENT=3;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_absbusinesspbs`
-- ----------------------------
ALTER TABLE `pbs_dynamic_absbusinesspbs` AUTO_INCREMENT=5;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_absforpbs`
-- ----------------------------
ALTER TABLE `pbs_dynamic_absforpbs` AUTO_INCREMENT=6;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_absonline`
-- ----------------------------
ALTER TABLE `pbs_dynamic_absonline` AUTO_INCREMENT=13;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_absticketservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_absticketservice` AUTO_INCREMENT=20;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_accountservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_accountservice` AUTO_INCREMENT=16;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_accountwebapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_accountwebapi` AUTO_INCREMENT=125;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_cbs`
-- ----------------------------
ALTER TABLE `pbs_dynamic_cbs` AUTO_INCREMENT=37;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_cbsweb`
-- ----------------------------
ALTER TABLE `pbs_dynamic_cbsweb` AUTO_INCREMENT=50;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_cmsservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_cmsservice` AUTO_INCREMENT=2;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_crm`
-- ----------------------------
ALTER TABLE `pbs_dynamic_crm` AUTO_INCREMENT=94;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_crmbusinessapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_crmbusinessapi` AUTO_INCREMENT=338;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_crmservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_crmservice` AUTO_INCREMENT=7;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_fbsferry`
-- ----------------------------
ALTER TABLE `pbs_dynamic_fbsferry` AUTO_INCREMENT=33;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_fbsferryforcbs`
-- ----------------------------
ALTER TABLE `pbs_dynamic_fbsferryforcbs` AUTO_INCREMENT=18;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_ferryservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_ferryservice` AUTO_INCREMENT=27;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_flightservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_flightservice` AUTO_INCREMENT=14;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_hotelservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_hotelservice` AUTO_INCREMENT=13;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_ignite`
-- ----------------------------
ALTER TABLE `pbs_dynamic_ignite` AUTO_INCREMENT=44;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_infrastructureservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_infrastructureservice` AUTO_INCREMENT=6;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_lbsapp`
-- ----------------------------
ALTER TABLE `pbs_dynamic_lbsapp` AUTO_INCREMENT=21;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_lbsbooking`
-- ----------------------------
ALTER TABLE `pbs_dynamic_lbsbooking` AUTO_INCREMENT=59;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_lbsproduct`
-- ----------------------------
ALTER TABLE `pbs_dynamic_lbsproduct` AUTO_INCREMENT=116;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_marketrestapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_marketrestapi` AUTO_INCREMENT=20;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_motorestapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_motorestapi` AUTO_INCREMENT=61;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_motoservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_motoservice` AUTO_INCREMENT=3;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_motowebapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_motowebapi` AUTO_INCREMENT=10;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_packagecbservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_packagecbservice` AUTO_INCREMENT=5;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_packagefhservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_packagefhservice` AUTO_INCREMENT=28;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_packageservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_packageservice` AUTO_INCREMENT=14;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbsdynamich5`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbsdynamich5` AUTO_INCREMENT=50;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbsh5static`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbsh5static` AUTO_INCREMENT=53;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbsh5staticl`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbsh5staticl` AUTO_INCREMENT=55;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbsservice`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbsservice` AUTO_INCREMENT=6;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbswebdynamic`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbswebdynamic` AUTO_INCREMENT=123;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbswebstatic`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbswebstatic` AUTO_INCREMENT=105;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_pbswebstaticl`
-- ----------------------------
ALTER TABLE `pbs_dynamic_pbswebstaticl` AUTO_INCREMENT=97;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_rbs`
-- ----------------------------
ALTER TABLE `pbs_dynamic_rbs` AUTO_INCREMENT=19;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_report`
-- ----------------------------
ALTER TABLE `pbs_dynamic_report` AUTO_INCREMENT=744596;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_rmwebapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_rmwebapi` AUTO_INCREMENT=57;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_statistics`
-- ----------------------------
ALTER TABLE `pbs_dynamic_statistics` AUTO_INCREMENT=31881;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_subreport`
-- ----------------------------
ALTER TABLE `pbs_dynamic_subreport` AUTO_INCREMENT=1576359;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_subtestcase`
-- ----------------------------
ALTER TABLE `pbs_dynamic_subtestcase` AUTO_INCREMENT=498;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_subtestcase20180108`
-- ----------------------------
ALTER TABLE `pbs_dynamic_subtestcase20180108` AUTO_INCREMENT=498;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_systemhost`
-- ----------------------------
ALTER TABLE `pbs_dynamic_systemhost` AUTO_INCREMENT=153;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_systemhost20180108`
-- ----------------------------
ALTER TABLE `pbs_dynamic_systemhost20180108` AUTO_INCREMENT=153;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_tbsapp`
-- ----------------------------
ALTER TABLE `pbs_dynamic_tbsapp` AUTO_INCREMENT=43;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_tbsbookingapi`
-- ----------------------------
ALTER TABLE `pbs_dynamic_tbsbookingapi` AUTO_INCREMENT=170;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_tbsweb`
-- ----------------------------
ALTER TABLE `pbs_dynamic_tbsweb` AUTO_INCREMENT=86;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_template`
-- ----------------------------
ALTER TABLE `pbs_dynamic_template` AUTO_INCREMENT=57;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_testcase`
-- ----------------------------
ALTER TABLE `pbs_dynamic_testcase` AUTO_INCREMENT=2256;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_testcase_suite_1101`
-- ----------------------------
ALTER TABLE `pbs_dynamic_testcase_suite_1101` AUTO_INCREMENT=2680;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_testcase20180108`
-- ----------------------------
ALTER TABLE `pbs_dynamic_testcase20180108` AUTO_INCREMENT=2256;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_testsuite`
-- ----------------------------
ALTER TABLE `pbs_dynamic_testsuite` AUTO_INCREMENT=59;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_testsuite20180108`
-- ----------------------------
ALTER TABLE `pbs_dynamic_testsuite20180108` AUTO_INCREMENT=59;

-- ----------------------------
-- Auto increment value for `pbs_dynamic_updatehost`
-- ----------------------------
ALTER TABLE `pbs_dynamic_updatehost` AUTO_INCREMENT=2;

-- ----------------------------
-- Auto increment value for `soap_api_soapreport`
-- ----------------------------
ALTER TABLE `soap_api_soapreport` AUTO_INCREMENT=45;

-- ----------------------------
-- Auto increment value for `soap_api_soapsubreport`
-- ----------------------------
ALTER TABLE `soap_api_soapsubreport` AUTO_INCREMENT=45;

-- ----------------------------
-- Auto increment value for `soap_api_soapsubtestcases`
-- ----------------------------
ALTER TABLE `soap_api_soapsubtestcases` AUTO_INCREMENT=2;

-- ----------------------------
-- Auto increment value for `soap_api_soaptestcases`
-- ----------------------------
ALTER TABLE `soap_api_soaptestcases` AUTO_INCREMENT=4;
