-- MySQL Script generated by MySQL Workbench
-- Thu Nov 30 01:52:18 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_smart_traffic_light
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `db_smart_traffic_light` ;

-- -----------------------------------------------------
-- Schema db_smart_traffic_light
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_smart_traffic_light` DEFAULT CHARACTER SET utf8 ;
USE `db_smart_traffic_light` ;

-- -----------------------------------------------------
-- Table `db_smart_traffic_light`.`recordings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_smart_traffic_light`.`recordings` ;

CREATE TABLE IF NOT EXISTS `db_smart_traffic_light`.`recordings` (
  `recording_id` BIGINT NOT NULL AUTO_INCREMENT,
  `rpi_path` VARCHAR(50) NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`recording_id`))
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `db_smart_traffic_light`.`intersections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_smart_traffic_light`.`intersections` ;

CREATE TABLE IF NOT EXISTS `db_smart_traffic_light`.`intersections` (
  `intersection_id` BIGINT NOT NULL AUTO_INCREMENT,
  `avenue_status_1` VARCHAR(20) NULL,
  `avenue_status_2` VARCHAR(20) NULL,
  `number_vehicles` INT NULL,
  `traffic_level` VARCHAR(20) NULL,
  `recording_id` BIGINT NOT NULL,
  PRIMARY KEY (`intersection_id`),
  INDEX `fk_intersections_recordings_idx` (`recording_id` ASC) VISIBLE)
ENGINE = MyISAM;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

