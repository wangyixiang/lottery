CREATE DATABASE IF NOT EXISTS `lotterydata`;

USE `lotterydata`;

DROP TABLE IF EXISTS `ssqdata`;
CREATE TABLE `ssqdata` (
    `drawnum` CHAR(7) NOT NULL PRIMARY KEY,
    `drawdate` DATE NOT NULL UNIQUE,
    `redball1` CHAR(2) NOT NULL,
    `redball2` CHAR(2) NOT NULL,
    `redball3` CHAR(2) NOT NULL,
    `redball4` CHAR(2) NOT NULL,
    `redball5` CHAR(2) NOT NULL,
    `redball6` CHAR(2) NOT NULL,
    `blueball1` CHAR(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `dltdata`;
CREATE TABLE `dltdata` (
    `drawnum` CHAR(7) NOT NULL PRIMARY KEY,
    `drawdate` DATE NOT NULL UNIQUE,
    `redball1` CHAR(2) NOT NULL,
    `redball2` CHAR(2) NOT NULL,
    `redball3` CHAR(2) NOT NULL,
    `redball4` CHAR(2) NOT NULL,
    `redball5` CHAR(2) NOT NULL,
    `blueball1` CHAR(2) NOT NULL,
    `blueball2` CHAR(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `genssqdata`;
#CREATE TABLE `genssqdata` (

#) ENGINE=InnoDB DEFAULT CHARSET=utf8;


#DROP TABLE IF EXISTS `gendltdata`;
#CREATE TABLE `gendltdata` (

#) ENGINE=InnoDB DEFAULT CHARSET=utf8;