-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema agrihire
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `agrihire` ;

-- -----------------------------------------------------
-- Schema agrihire
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `agrihire` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `agrihire` ;

-- -----------------------------------------------------
-- Table `agrihire`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('customer', 'staff', 'lmgr', 'nmgr', 'admin') NOT NULL,
  `is_active` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`staff` (
  `staff_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `store_id` INT NULL DEFAULT NULL,
  `first_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `position` VARCHAR(255) NULL DEFAULT NULL,
  `phone` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `store_id` (`store_id` ASC) VISIBLE,
  CONSTRAINT `staff_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `agrihire`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `staff_ibfk_2`
    FOREIGN KEY (`store_id`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`store` (
  `store_id` INT NOT NULL AUTO_INCREMENT,
  `store_name` VARCHAR(50) NOT NULL,
  `phone` VARCHAR(20) NULL DEFAULT NULL,
  `email` VARCHAR(50) NULL DEFAULT NULL,
  `address_line1` VARCHAR(255) NULL DEFAULT NULL,
  `address_line2` VARCHAR(255) NULL DEFAULT NULL,
  `suburb` VARCHAR(50) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `post_code` VARCHAR(10) NULL DEFAULT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  `manager_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`store_id`),
  UNIQUE INDEX `store_name_UNIQUE` (`store_name` ASC) VISIBLE,
  INDEX `store_ibfk_1_idx` (`manager_id` ASC) VISIBLE,
  CONSTRAINT `store_ibfk_1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `agrihire`.`staff` (`staff_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `first_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `phone` VARCHAR(20) NULL DEFAULT NULL,
  `address_line1` VARCHAR(255) NULL DEFAULT NULL,
  `address_line2` VARCHAR(255) NULL DEFAULT NULL,
  `suburb` VARCHAR(50) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `post_code` VARCHAR(10) NULL DEFAULT NULL,
  `my_store` INT NULL,
  PRIMARY KEY (`customer_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `customer_ibfk_2_idx` (`my_store` ASC) VISIBLE,
  CONSTRAINT `customer_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `agrihire`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `customer_ibfk_2`
    FOREIGN KEY (`my_store`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`booking` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `create_date` DATETIME NOT NULL,
  `total` DECIMAL(10,2) NOT NULL,
  `note` VARCHAR(255) NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`booking_id`),
  INDEX `customer_id` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `booking_ibfk_1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `agrihire`.`customer` (`customer_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`category` (
  `category_code` VARCHAR(10) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`category_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`product` (
  `product_code` VARCHAR(20) NOT NULL,
  `category_code` VARCHAR(10) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `desc` TEXT NULL DEFAULT NULL,
  `specs` TEXT NULL DEFAULT NULL,
  `price_a` DECIMAL(10,2) NOT NULL,
  `qty_break_a` INT NOT NULL DEFAULT 0,
  `price_b` DECIMAL(10,2) NULL DEFAULT NULL,
  `qty_break_b` INT NULL DEFAULT 168,
  `price_c` DECIMAL(10,2) NULL DEFAULT NULL,
  `qty_break_c` INT NULL DEFAULT 600,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`product_code`),
  INDEX `category_id` (`category_code` ASC) VISIBLE,
  CONSTRAINT `product_ibfk_1`
    FOREIGN KEY (`category_code`)
    REFERENCES `agrihire`.`category` (`category_code`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`machine`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`machine` (
  `machine_id` INT NOT NULL AUTO_INCREMENT,
  `sn` VARCHAR(50) NOT NULL,
  `product_code` VARCHAR(20) NOT NULL,
  `store_id` INT NOT NULL,
  `purchase_date` DATE NULL DEFAULT NULL,
  `cost` DECIMAL(10,2) NULL DEFAULT NULL,
  `photo` VARCHAR(255) NULL DEFAULT NULL,
  `condition` VARCHAR(100) NULL DEFAULT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`machine_id`),
  INDEX `product_id` (`product_code` ASC) VISIBLE,
  INDEX `store_id` (`store_id` ASC) VISIBLE,
  INDEX `sn` (`sn` ASC) VISIBLE,
  CONSTRAINT `machine_ibfk_1`
    FOREIGN KEY (`product_code`)
    REFERENCES `agrihire`.`product` (`product_code`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `machine_ibfk_2`
    FOREIGN KEY (`store_id`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`booking_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`booking_item` (
  `booking_item_id` INT NOT NULL AUTO_INCREMENT,
  `booking_id` INT NOT NULL,
  `machine_id` INT NOT NULL,
  `line_num` INT NOT NULL,
  `hire_rate` DECIMAL(10,2) NOT NULL,
  `hire_from` DATETIME NOT NULL,
  `hire_to` DATETIME NOT NULL,
  PRIMARY KEY (`booking_item_id`),
  INDEX `booking_id` (`booking_id` ASC) VISIBLE,
  INDEX `machine_id` (`machine_id` ASC) VISIBLE,
  CONSTRAINT `booking_item_ibfk_1`
    FOREIGN KEY (`booking_id`)
    REFERENCES `agrihire`.`booking` (`booking_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `booking_item_ibfk_2`
    FOREIGN KEY (`machine_id`)
    REFERENCES `agrihire`.`machine` (`machine_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`cart` (
  `cart_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`cart_id`),
  INDEX `customer_id` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `cart_ibfk_1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `agrihire`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`cart_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`cart_item` (
  `cart_item_id` INT NOT NULL AUTO_INCREMENT,
  `cart_id` INT NOT NULL,
  `prodouct_code` VARCHAR(20) NOT NULL,
  `qty` INT NOT NULL,
  `line_num` INT NOT NULL,
  `hire_rate` DECIMAL(10,2) NOT NULL,
  `hire_from` DATETIME NOT NULL,
  `hire_to` DATETIME NOT NULL,
  PRIMARY KEY (`cart_item_id`),
  INDEX `cart_id` (`cart_id` ASC) VISIBLE,
  INDEX `carrt_item_ibfk_2_idx` (`prodouct_code` ASC) VISIBLE,
  CONSTRAINT `cart_item_ibfk_1`
    FOREIGN KEY (`cart_id`)
    REFERENCES `agrihire`.`cart` (`cart_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `cart_item_ibfk_2`
    FOREIGN KEY (`prodouct_code`)
    REFERENCES `agrihire`.`product` (`product_code`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`hire_record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`hire_record` (
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `booking_item_id` INT NOT NULL,
  `checkout_time` DATETIME NULL DEFAULT NULL,
  `checkout_staff` INT NULL DEFAULT NULL,
  `return_time` DATETIME NULL DEFAULT NULL,
  `return_staff` INT NULL DEFAULT NULL,
  `note` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  INDEX `hire_record_ibfk_1_idx` (`booking_item_id` ASC) VISIBLE,
  INDEX `hire_record_ibfk_2_idx` (`checkout_staff` ASC) VISIBLE,
  INDEX `hire_record_ibfk_3_idx` (`return_staff` ASC) VISIBLE,
  CONSTRAINT `hire_record_ibfk_1`
    FOREIGN KEY (`booking_item_id`)
    REFERENCES `agrihire`.`booking_item` (`booking_item_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `hire_record_ibfk_2`
    FOREIGN KEY (`checkout_staff`)
    REFERENCES `agrihire`.`staff` (`staff_id`),
  CONSTRAINT `hire_record_ibfk_3`
    FOREIGN KEY (`return_staff`)
    REFERENCES `agrihire`.`staff` (`staff_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`message` (
  `message_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `store_id` INT NOT NULL,
  `subject` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `create_date` DATETIME NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`message_id`),
  INDEX `customer_id` (`customer_id` ASC) VISIBLE,
  INDEX `message_ibfk_2_idx` (`store_id` ASC) VISIBLE,
  CONSTRAINT `message_ibfk_1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `agrihire`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `message_ibfk_2`
    FOREIGN KEY (`store_id`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`news`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`news` (
  `news_id` INT NOT NULL AUTO_INCREMENT,
  `store_id` INT NOT NULL,
  `title` VARCHAR(255) NULL DEFAULT NULL,
  `content` TEXT NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`news_id`),
  INDEX `news_ibfk_1_idx` (`store_id` ASC) VISIBLE,
  CONSTRAINT `news_ibfk_1`
    FOREIGN KEY (`store_id`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`payment` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `booking_id` INT NOT NULL,
  `create_date` DATETIME NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `payment_ibfk_1_idx` (`booking_id` ASC) VISIBLE,
  CONSTRAINT `payment_ibfk_1`
    FOREIGN KEY (`booking_id`)
    REFERENCES `agrihire`.`booking` (`booking_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`promotion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`promotion` (
  `promo_code` VARCHAR(10) NOT NULL,
  `store_id` INT NOT NULL,
  `disc_rate` DECIMAL(10,2) NOT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  `desc` VARCHAR(255) NULL DEFAULT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`promo_code`),
  INDEX `promotion_ibfk_1_idx` (`store_id` ASC) VISIBLE,
  CONSTRAINT `promotion_ibfk_1`
    FOREIGN KEY (`store_id`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`promo_category`
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS `agrihire`.`promo_category` (
--   `promo_code` VARCHAR(10) NOT NULL,
--   `category_code` VARCHAR(10) NOT NULL,
--   PRIMARY KEY (`promo_code`, `category_code`),
--   INDEX `promotion_id` (`promo_code` ASC) VISIBLE,
--   INDEX `promotion_record_ibfk_20_idx` (`category_code` ASC) VISIBLE,
--   CONSTRAINT `promo_category_ibfk_1`
--     FOREIGN KEY (`promo_code`)
--     REFERENCES `agrihire`.`promotion` (`promo_code`)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE,
--   CONSTRAINT `promo_category_ibfk_2`
--     FOREIGN KEY (`category_code`)
--     REFERENCES `agrihire`.`category` (`category_code`)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE)
-- ENGINE = InnoDB
-- DEFAULT CHARACTER SET = utf8mb4
-- COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`promo_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`promo_product` (
  `promo_code` VARCHAR(10) NOT NULL,
  `product_code` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`promo_code`, `product_code`),
  INDEX `promotion_id` (`promo_code` ASC) VISIBLE,
  INDEX `product_id` (`product_code` ASC) VISIBLE,
  CONSTRAINT `promo_product_ibfk_1`
    FOREIGN KEY (`promo_code`)
    REFERENCES `agrihire`.`promotion` (`promo_code`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `promo_product_ibfk_2`
    FOREIGN KEY (`product_code`)
    REFERENCES `agrihire`.`product` (`product_code`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`service` (
  `service_id` INT NOT NULL AUTO_INCREMENT,
  `machine_id` INT NOT NULL,
  `service_date` DATE NOT NULL,
  `service_name` VARCHAR(255) NOT NULL,
  `note` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`service_id`),
  INDEX `machine_id` (`machine_id` ASC) VISIBLE,
  CONSTRAINT `service_ibfk_1`
    FOREIGN KEY (`machine_id`)
    REFERENCES `agrihire`.`machine` (`machine_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`setting`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`setting` (
  `setting_id` INT NOT NULL AUTO_INCREMENT,
  `setting_key` VARCHAR(255) NOT NULL,
  `setting_value` VARCHAR(255) NOT NULL,
  `desc` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`setting_id`),
  UNIQUE INDEX `setting_key_UNIQUE` (`setting_key` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `agrihire`.`store_hour`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agrihire`.`store_hour` (
  `store_id` INT NOT NULL,
  `week_day` INT NOT NULL,
  `open_time` TIME NOT NULL,
  `close_time` TIME NOT NULL,
  PRIMARY KEY (`store_id`, `week_day`),
  CONSTRAINT `store_hour_ibfk_1`
    FOREIGN KEY (`store_id`)
    REFERENCES `agrihire`.`store` (`store_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;