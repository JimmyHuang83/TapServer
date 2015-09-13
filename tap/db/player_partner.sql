/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : tap_titan_game

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-05-15 13:27:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for player_partner
-- ----------------------------
DROP TABLE IF EXISTS `player_partner`;
CREATE TABLE `player_partner` (
  `player_id` int(255) NOT NULL,
  `partner_id` int(10) NOT NULL,
  `level` int(10) DEFAULT NULL,
  `hadBeenUnlocked` int(1) DEFAULT '0',
  `hp` int(5) DEFAULT '100',
  PRIMARY KEY (`player_id`,`partner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of player_partner
-- ----------------------------
INSERT INTO `player_partner` VALUES ('10038', '1', '1', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '2', '1', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '3', '1', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '4', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '5', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '6', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '7', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '8', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '9', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '10', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '11', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '12', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '13', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '14', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '15', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '16', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '17', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '18', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '19', '0', '0', '100');
INSERT INTO `player_partner` VALUES ('10038', '20', '0', '0', '100');
