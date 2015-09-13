/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : tap_titan_game

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-05-28 10:02:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_global_base
-- ----------------------------
DROP TABLE IF EXISTS `table_global_base`;
CREATE TABLE `table_global_base` (
  `id` varchar(30) NOT NULL,
  `value` int(7) DEFAULT NULL,
  `description` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of table_global_base
-- ----------------------------
INSERT INTO `table_global_base` VALUES ('AdTriInterval', '120', '广告间隔');
INSERT INTO `table_global_base` VALUES ('AvoidMax', '700', '闪避上限');
INSERT INTO `table_global_base` VALUES ('BaseAvoid', '10', '基础闪避');
INSERT INTO `table_global_base` VALUES ('BaseCrital', '10', '基础暴击值');
INSERT INTO `table_global_base` VALUES ('BaseCritalRate', '10', '基础暴击伤害倍率');
INSERT INTO `table_global_base` VALUES ('CritalMax', '800', '最大暴击值');
INSERT INTO `table_global_base` VALUES ('daily_challenge_num', '10', '每日挑战最大次数');
INSERT INTO `table_global_base` VALUES ('equipment_buff_maxrate', '120', '装备buff随机范围正太常量');
INSERT INTO `table_global_base` VALUES ('equipment_buff_minrate', '80', '装备buff随机范围正太常量');
INSERT INTO `table_global_base` VALUES ('equipment_fullrecycle_cost', '100', '100%分解消耗宝石/次');
INSERT INTO `table_global_base` VALUES ('equipment_recycle_discount', '50', '装备分解打折系数(%)');
INSERT INTO `table_global_base` VALUES ('MAX_LENGTH_OF_NAME', '7', '玩家名字最长长度(汉字算2个字符)');
INSERT INTO `table_global_base` VALUES ('RandomRewardDailyMaxTimes', '100', '小仙女每天最大次数');
INSERT INTO `table_global_base` VALUES ('ZsbuyGoldRate', '5000', '钻石买金倍率');
