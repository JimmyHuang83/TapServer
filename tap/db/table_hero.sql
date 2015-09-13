/*
Navicat MySQL Data Transfer

Source Server         : AwsFree
Source Server Version : 50538
Source Host           : 54.169.92.200:3306
Source Database       : tap_titan_game_o2

Target Server Type    : MYSQL
Target Server Version : 50538
File Encoding         : 65001

Date: 2015-05-15 14:32:41
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_hero
-- ----------------------------
DROP TABLE IF EXISTS `table_hero`;
CREATE TABLE `table_hero` (
  `id` int(4) NOT NULL,
  `atkinterval` int(4) DEFAULT NULL,
  `dps` int(4) DEFAULT NULL,
  `propmodify` varchar(10) DEFAULT NULL,
  `skills` varchar(60) DEFAULT NULL,
  `upgrade_cost_modify` varchar(10) DEFAULT NULL,
  `cost_type` int(10) DEFAULT NULL,
  `cost_value` varchar(60) DEFAULT NULL,
  `hp` int(10) DEFAULT '100',
  `sub_hp` int(10) DEFAULT '1',
  `add_hp` int(10) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of table_hero
-- ----------------------------
INSERT INTO `table_hero` VALUES ('1', '3', '2', '3.1', '2,2,10,11,12,13,14', '1.1', '1', '100', '100', '2', '2');
INSERT INTO `table_hero` VALUES ('2', '2', '2', '3.2', '3,3,17,18,19,20,21', '1.1', '1', '100', '100', '3', '3');
INSERT INTO `table_hero` VALUES ('3', '2', '2', '2.9', '4,4,24,25,26,27,28', '1.1', '1', '100', '100', '4', '4');
INSERT INTO `table_hero` VALUES ('4', '4', '2', '3.1', '5,5,31,32,33,34,35', '1.1', '1', '100', '100', '5', '5');
INSERT INTO `table_hero` VALUES ('5', '4', '2', '3.1', '6,6,38,39,40,41,42', '1.1', '1', '100', '100', '6', '6');
INSERT INTO `table_hero` VALUES ('6', '4', '2', '3.8', '7,7,45,46,47,48,49', '1.1', '1', '100', '100', '7', '7');
INSERT INTO `table_hero` VALUES ('7', '3', '2', '3.9', '8,8,52,53,54,55,56', '1.1', '1', '100', '100', '8', '8');
INSERT INTO `table_hero` VALUES ('8', '4', '2', '3.5', '9,9,59,60,61,62,63', '1.1', '1', '100', '100', '9', '9');
INSERT INTO `table_hero` VALUES ('9', '4', '2', '3.5', '10,10,66,67,68,69,70', '1.1', '1', '100', '100', '10', '10');
INSERT INTO `table_hero` VALUES ('10', '2', '2', '3.5', '11,11,73,74,75,76,77', '1.1', '1', '100', '100', '11', '11');
INSERT INTO `table_hero` VALUES ('11', '2', '2', '3.5', '12,12,80,81,82,83,84', '1.1', '1', '100', '100', '12', '12');
INSERT INTO `table_hero` VALUES ('12', '3', '2', '3.9', '13,13,87,88,89,90,91', '1.1', '1', '100', '100', '13', '13');
INSERT INTO `table_hero` VALUES ('13', '3', '2', '3.6', '14,14,94,95,96,97,98', '1.1', '1', '100', '100', '14', '14');
INSERT INTO `table_hero` VALUES ('14', '3', '2', '3.6', '15,15,101,102,103,104,105', '1.1', '1', '100', '100', '15', '15');
INSERT INTO `table_hero` VALUES ('15', '3', '2', '3.6', '16,16,108,109,110,111,112', '1.1', '1', '100', '100', '16', '16');
INSERT INTO `table_hero` VALUES ('16', '3', '2', '4.16', '17,17,115,116,117,118,119', '1.1', '1', '100', '100', '17', '17');
INSERT INTO `table_hero` VALUES ('17', '3', '2', '4.15', '18,18,122,123,124,125,126', '1.1', '1', '100', '100', '18', '18');
INSERT INTO `table_hero` VALUES ('18', '3', '2', '4.15', '19,19,129,130,131,132,133', '1.1', '1', '100', '100', '19', '19');
INSERT INTO `table_hero` VALUES ('19', '3', '2', '4.2', '20,20,136,137,138,139,140', '1.1', '1', '100', '100', '20', '20');
INSERT INTO `table_hero` VALUES ('20', '3', '2', '4.15', '21,21,143,144,145,146,147', '1.1', '1', '100', '100', '21', '21');
INSERT INTO `table_hero` VALUES ('50000', '0', '1', '1.1', '1,1,3,4,5,6,7', '1.1', '1', '100', '100', '1', '1');
