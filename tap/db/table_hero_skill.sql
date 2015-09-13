/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : tap_titan_game

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2015-04-22 17:50:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_hero_skill
-- ----------------------------
DROP TABLE IF EXISTS `table_hero_skill`;
CREATE TABLE `table_hero_skill` (
  `table_hero_skill_id` int(4) NOT NULL,
  `skill_level` int(4) NOT NULL,
  `unlock_level` int(7) DEFAULT NULL,
  `upcost` int(20) DEFAULT NULL,
  `type` int(1) DEFAULT NULL,
  `cd` int(4) DEFAULT NULL,
  `duration` int(4) DEFAULT NULL,
  `trigglerate` int(4) DEFAULT NULL,
  `applytimes` int(4) DEFAULT NULL,
  `applytarget` int(4) DEFAULT NULL,
  `applaytargetnum` int(4) DEFAULT NULL,
  `effecttype0` int(3) DEFAULT NULL,
  `effectvalue0` int(3) DEFAULT NULL,
  `buffvalue0` int(3) DEFAULT NULL,
  `spawnnewid` int(3) DEFAULT NULL,
  PRIMARY KEY (`table_hero_skill_id`,`skill_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of table_hero_skill
-- ----------------------------
INSERT INTO `table_hero_skill` VALUES ('1', '1', '20', '250', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '2', '30', '386', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '3', '40', '526', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '4', '50', '672', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '5', '60', '826', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '6', '70', '3060', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '7', '80', '6154', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '8', '90', '9974', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '9', '100', '14608', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('1', '10', '110', '20206', '0', '10', '0', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '1', '30', '408', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '2', '40', '562', '0', '10', '3', '101', '2', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '3', '50', '710', '0', '10', '3', '102', '3', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '4', '60', '1140', '0', '10', '3', '103', '4', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '5', '70', '3626', '0', '10', '3', '104', '5', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '6', '80', '6818', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '7', '90', '10874', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '8', '100', '15680', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '9', '110', '21320', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('2', '10', '120', '28028', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '1', '40', '586', '0', '30', '20', '100', '1', '0', '1', '0', '1500', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '2', '50', '736', '0', '30', '22', '100', '1', '0', '1', '0', '2000', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '3', '60', '1574', '0', '30', '24', '100', '1', '0', '1', '0', '2500', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '4', '70', '4174', '0', '30', '26', '100', '1', '0', '1', '0', '3000', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '5', '80', '7582', '0', '30', '28', '100', '1', '0', '1', '0', '3500', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '6', '90', '11708', '0', '30', '30', '100', '1', '0', '1', '0', '4000', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '7', '100', '16786', '0', '30', '32', '100', '1', '0', '1', '0', '4500', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '8', '110', '22622', '0', '30', '34', '100', '1', '0', '1', '0', '5000', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '9', '120', '29340', '0', '30', '36', '100', '1', '0', '1', '0', '5500', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('3', '10', '130', '37216', '0', '30', '38', '100', '1', '0', '1', '0', '6000', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '1', '50', '762', '0', '30', '20', '100', '1', '0', '1', '0', '30', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '2', '60', '2046', '0', '30', '22', '100', '1', '0', '1', '0', '40', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '3', '70', '4796', '0', '30', '24', '100', '1', '0', '1', '0', '50', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '4', '80', '8366', '0', '30', '26', '100', '1', '0', '1', '0', '60', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '5', '90', '12672', '0', '30', '28', '100', '1', '0', '1', '0', '70', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '6', '100', '17800', '0', '30', '30', '100', '1', '0', '1', '0', '80', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '7', '110', '23946', '0', '30', '32', '100', '1', '0', '1', '0', '90', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '8', '120', '30870', '0', '30', '34', '100', '1', '0', '1', '0', '100', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '9', '130', '38732', '0', '30', '36', '100', '1', '0', '1', '0', '110', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('4', '10', '140', '47822', '0', '30', '38', '100', '1', '0', '1', '0', '120', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '1', '60', '2520', '0', '60', '20', '100', '1', '0', '1', '0', '30', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '2', '70', '5460', '0', '60', '22', '100', '1', '0', '1', '0', '40', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '3', '80', '9118', '0', '60', '24', '100', '1', '0', '1', '0', '50', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '4', '90', '13678', '0', '60', '26', '100', '1', '0', '1', '0', '60', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '5', '100', '18986', '0', '60', '28', '100', '1', '0', '1', '0', '70', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '6', '110', '25164', '0', '60', '30', '100', '1', '0', '1', '0', '80', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '7', '120', '32450', '0', '60', '32', '100', '1', '0', '1', '0', '90', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '8', '130', '40516', '0', '60', '34', '100', '1', '0', '1', '0', '100', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '9', '140', '49570', '0', '60', '36', '100', '1', '0', '1', '0', '110', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('5', '10', '150', '59946', '0', '60', '38', '100', '1', '0', '1', '0', '120', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '1', '70', '5770', '0', '180', '5', '100', '1', '0', '1', '0', '1', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '2', '80', '9588', '0', '180', '5', '100', '1', '0', '1', '0', '2', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '3', '90', '14142', '0', '180', '5', '100', '1', '0', '1', '0', '3', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '4', '100', '19518', '0', '180', '5', '100', '1', '0', '1', '0', '4', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '5', '110', '25950', '0', '180', '5', '100', '1', '0', '1', '0', '5', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '6', '120', '33158', '0', '180', '5', '100', '1', '0', '1', '0', '6', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '7', '130', '41304', '0', '180', '5', '100', '1', '0', '1', '0', '7', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '8', '140', '50716', '0', '180', '5', '100', '1', '0', '1', '0', '8', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '9', '150', '60932', '0', '180', '5', '100', '1', '0', '1', '0', '9', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('6', '10', '160', '72532', '0', '180', '5', '100', '1', '0', '1', '0', '10', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('7', '1', '80', '6154', '0', '600', '0', '100', '1', '0', '1', '4', '0', '0', '0');
INSERT INTO `table_hero_skill` VALUES ('8', '1', '30', '386', '0', '10', '3', '100', '1', '0', '1', '0', '0', '0', '0');
