-- MySQL Script generated by MySQL Workbench
-- mar. 30 janv. 2018 09:14:08 CET
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema gazetteer
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `gazetteer` ;

-- -----------------------------------------------------
-- Schema gazetteer
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gazetteer` DEFAULT CHARACTER SET utf8 ;
USE `gazetteer` ;

-- -----------------------------------------------------
-- Table `gazetteer`.`place`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`place` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`place` (
  `place_id` INT NOT NULL AUTO_INCREMENT COMMENT '	',
  `place_nom` TINYTEXT NOT NULL,
  `place_description` TEXT NULL,
  `place_longitude` FLOAT NOT NULL,
  `place_latitude` FLOAT NOT NULL,
  `place_type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`place_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gazetteer`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`user` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `user_nom` TINYTEXT NOT NULL,
  `user_login` VARCHAR(45) NOT NULL,
  `user_email` TINYTEXT NOT NULL,
  `user_password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_login_UNIQUE` (`user_login` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gazetteer`.`authorship`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`authorship` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`authorship` (
  `authorship_id` INT NOT NULL AUTO_INCREMENT,
  `authorship_user_id` INT NOT NULL,
  `authorship_place_id` INT NOT NULL,
  `authorship_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`authorship_id`),
  INDEX `fk_authorship_1_idx` (`authorship_place_id` ASC),
  INDEX `fk_authorship_2_idx` (`authorship_user_id` ASC),
  CONSTRAINT `fk_authorship_1`
    FOREIGN KEY (`authorship_place_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_authorship_2`
    FOREIGN KEY (`authorship_user_id`)
    REFERENCES `gazetteer`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `gazetteer`.`relation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`relation` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`relation` (
  `relation_id` INT NOT NULL AUTO_INCREMENT,
  `relation_biblio_id` INT NOT NULL,
  `relation_place_id` INT NOT NULL,
  PRIMARY KEY (`relation_id`),
  INDEX `fk_relation_1_idx` (`relation_place_id` ASC),
  INDEX `fk_relation_2_idx` (`relation_biblio_id` ASC),
  CONSTRAINT `fk_relation_1`
    FOREIGN KEY (`relation_place_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_relation_2`
    FOREIGN KEY (`relation_biblio_id`)
    REFERENCES `gazetteer`.`biblio` (`biblio_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- ----------------------------------------------------
-- Table `gazetteer`.`biblio`
-- ----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`biblio` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`biblio` (
  `biblio_id` INT NOT NULL AUTO_INCREMENT COMMENT '	',
  `biblio_titre` TEXT NOT NULL,
  `biblio_auteur` TEXT NOT NULL,
  `biblio_date` TEXT NULL,
  `biblio_lieu` TEXT NULL,
  `biblio_type` TEXT NOT NULL,
  PRIMARY KEY (`biblio_id`))
ENGINE = InnoDB;
COMMIT;

-- -----------------------------------------------------
-- Table `gazetteer`.`link`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`link` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link` (
  `link_id` INT NOT NULL AUTO_INCREMENT,
  `nature_id` INT NOT NULL,
  `link_place1_id` INT NOT NULL,
  `link_place2_id` INT NOT NULL,
  PRIMARY KEY (`link_id`),
  INDEX `fk_link_1_idx` (`nature_id` ASC),
  INDEX `fk_link_2_idx` (`link_place1_id` ASC),
  INDEX `fk_link_3_idx` (`link_place2_id` ASC),
  CONSTRAINT `fk_link_1`
    FOREIGN KEY (`nature_id`)
    REFERENCES `gazetteer`.`link_relation` (`nature_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_link_2`
    FOREIGN KEY (`link_place1_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    CONSTRAINT `fk_link_3`
      FOREIGN KEY (`link_place2_id`)
      REFERENCES `gazetteer`.`place` (`place_id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `gazetteer`.`link_relation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`link_relation` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link` (
  `nature_id` INT NOT NULL AUTO_INCREMENT,
  `link_relation_type` VARCHAR(45) NOT NULL,
  `link_relation_description` VARCHAR(240),
  PRIMARY KEY (`nature_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `gazetteer`.`variante`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`variante` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`variante` (
  `variante_id` INT NOT NULL AUTO_INCREMENT,
  `variante_nom` TINYTEXT NOT NULL,
  `variante_lang_code` VARCHAR(45) NOT NULL,
  `variante_place_id` INT NOT NULL,
  PRIMARY KEY (`variante_id`),
  INDEX `fk_variante_1_idx` (`variante_place_id` ASC),
  CONSTRAINT `fk_variante_1`
    FOREIGN KEY (`variante_place_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE = '';
GRANT USAGE ON *.* TO gazetteer_user;
 DROP USER gazetteer_user;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'gazetteer_user' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON `gazetteer`.* TO 'gazetteer_user';
GRANT SELECT ON TABLE `gazetteer`.* TO 'gazetteer_user';
GRANT SELECT, INSERT, TRIGGER ON TABLE `gazetteer`.* TO 'gazetteer_user';
GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `gazetteer`.* TO 'gazetteer_user';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `gazetteer`.`place`
-- -----------------------------------------------------
START TRANSACTION;
USE `gazetteer`;
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Hippana', 'Ancient settlement in the western part of Sicily, probably founded in the seventh century B.C.', 37.7018481, 13.4357804, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Nicomedia', 'Nicomedia was founded in 712/11 BC as a Megarian colony named Astacus and was rebuilt by Nicomedes I of Bithynia in 264 BC. The city was an important administrative center of the Roman Empire.', 40.7651905, 29.919887000000003, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Aornos', 'Aornos was a mountain fortress and the site of Alexander the Great\'s last siege during the winter of 327-6 BC. The ancient site likely corresponds to Ūṇa, a peak on the Pīr-Sar west of the Indus river.', 34.75257, 72.803461, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'The \"Hochtor Sanctuary\"', 'A Celto-Roman sanctuary situated at an ancient high-mountain pass in the eastern Alps near Grossglockner, excavated beginning in the 1990s. Its ancient name is unknown.', 47.081765, 12.842636, 'sanctuary');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Lipara (settlement)', 'A Greek colony and long-time settlement on the island of the same name, located to the north of Sicily in the Tyrrhenian Sea. Modern Lipari.', 38.46740105, 14.953957299999999, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Arch of Constantine', 'The Arch of Constantine at Rome, a triumphal arch dedicated in A.D. 315.', 41.889892, 12.4904941, 'arch');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Taberna Pomaria di Felix', 'A fruit shop in Pompeii (I, 8, 1) with an entrance on to the Via dell\'Abbondanza.', 40.75074883061887, 14.48995445324075, 'taberna-shop');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'S. Paulus', 'One of Rome\'s four major papal basilicae, S. Paulus was founded by Constantine I in the early fourth century A.D. and expanded by Valentinian I in the 370s.', 41.858695, 12.476827, 'church');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Calleva', 'Calleva Atrebatum (known as Silchester Roman Town) was an Iron Age oppidum and Roman town in  Britannia. It was the civitas capital of the Atrebates tribe.', 51.35546, -1.0915195, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Colophon/Colophon ad Mare/Notion', 'A port city founded by Aeolian settlers at the mouth of the River Avci.', 37.9928, 27.1975, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Bousiris', 'Bousiris was a city of Lower Egypt near the Phatnitic mouth of the Nile river and was considered one of the possible birthplaces of Osiris.', 30.913368, 31.238795500000002, 'settlement');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Corinthia', 'Corinthia was a region of ancient Greece associated with the city-state Corinth.', 37.798572, 22.834379, 'region');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Garumna (river)', 'The Garonne river is a river of southwestern Gaul and northern Iberia.', 44.810025550000006, -0.3184549, 'river');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Caelius Mons', 'The Caelian Hill in Rome.', 41.88755097676503, 12.491300775912759, 'hill');
INSERT INTO `gazetteer`.`place` ( `place_nom`, `place_description`, `place_longitude`, `place_latitude`, `place_type`) VALUES ( 'Prinias (Patela)', 'An Iron Age settlement on the Patela plateau north of the modern village of Prinias; its ancient name is uncertain. The site is notable for its occupation from the end of the Bronze Age through to the Archaic period, as well as for the monumental architecture and Orientalizing sculpture of its Buildings (\'Temples\') A and B. ', 35.168633, 25.000922, 'settlement');

INSERT INTO `gazetteer`.`biblio` (`biblio_id`,`biblio_titre`, `biblio_auteur`, `biblio_date`, `biblio_lieu`, `biblio_type`) VALUES ( 1, 'Versailles, un palais pour la sculpture', 'Alexandre Maral', '2013', 'Dijon', 'art history');
INSERT INTO `gazetteer`.`biblio` (`biblio_id`,`biblio_titre`, `biblio_auteur`, `biblio_date`, `biblio_lieu`, `biblio_type`) VALUES ( 2, 'The Banquet', 'Platon', 'Ve BC.', 'Athens', 'philosophical treaty');
INSERT INTO `gazetteer`.`biblio` (`biblio_id`,`biblio_titre`, `biblio_auteur`, `biblio_date`, `biblio_lieu`, `biblio_type`) VALUES ( 3, 'Le Phèdre','Platon', 'Ve BC.', 'Athens', 'philosophical treaty');
INSERT INTO `gazetteer`.`biblio` (`biblio_id`, `biblio_titre`, `biblio_auteur`, `biblio_date`, `biblio_lieu`, `biblio_type`) VALUES ( 4, 'The Iliad', 'Homer', '', '', 'epic');
INSERT INTO `gazetteer`.`biblio` (`biblio_id`, `biblio_titre`, `biblio_auteur`, `biblio_date`, `biblio_lieu`, `biblio_type`) VALUES ( 5, 'The Odyssey', 'Homer', '', '', 'epic');
INSERT INTO `gazetteer`.`biblio` (`biblio_id`, `biblio_titre`, `biblio_auteur`, `biblio_date`, `biblio_lieu`, `biblio_type`) VALUES ( 6, 'Works and Days', 'Hesiod', '', '', 'poem');

INSERT INTO `gazetteer`.`relation` (`relation_id`, `relation_biblio_id`, `relation_place_id`) VALUES ('1', '1', '1');

COMMIT;


-- -----------------------------------------------------
-- Data for table `gazetteer`.`user`
-- -----------------------------------------------------
START TRANSACTION;
USE `gazetteer`;
INSERT INTO `gazetteer`.`user` (`user_id`, `user_nom`, `user_login`, `user_email`, `user_password`) VALUES (1, 'Administrator', 'admin', 'admin@supersite.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

COMMIT;
