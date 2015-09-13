/*
Navicat MySQL Data Transfer

Source Server         : AwsFree
Source Server Version : 50538
Source Host           : 54.169.92.200:3306
Source Database       : tap_titan_login

Target Server Type    : MYSQL
Target Server Version : 50538
File Encoding         : 65001

Date: 2015-04-20 10:34:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for client_version
-- ----------------------------
DROP TABLE IF EXISTS `client_version`;
CREATE TABLE `client_version` (
  `version` varchar(5) NOT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of client_version
-- ----------------------------
INSERT INTO `client_version` VALUES ('0.3');

-- ----------------------------
-- Table structure for server
-- ----------------------------
DROP TABLE IF EXISTS `server`;
CREATE TABLE `server` (
  `serverid` int(200) NOT NULL,
  `serverip` varchar(20) DEFAULT NULL,
  `serverport` varchar(10) DEFAULT NULL,
  `servername` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`serverid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of server
-- ----------------------------
INSERT INTO `server` VALUES ('10000', '192.168.1.127', '16001', '内网测试1服');
INSERT INTO `server` VALUES ('20000', '54.169.92.200', '16001', '外网测试1服');
INSERT INTO `server` VALUES ('40000', '54.169.92.200', '16002', '外网测试2服');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'mike', 'abcd');
