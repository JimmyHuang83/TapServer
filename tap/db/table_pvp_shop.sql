/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : tap_titan_game

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-06-08 15:39:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_pvp_shop
-- ----------------------------
DROP TABLE IF EXISTS `table_pvp_shop`;
CREATE TABLE `table_pvp_shop` (
  `id` int(10) NOT NULL,
  `buy_item_id` int(10) DEFAULT NULL,
  `cost_type` int(10) DEFAULT NULL,
  `cost_value` int(10) DEFAULT NULL,
  `jump_ad` int(1) DEFAULT NULL,
  `jump_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of table_pvp_shop
-- ----------------------------
INSERT INTO `table_pvp_shop` VALUES ('1', '1', '1', '1', '1', '1');
