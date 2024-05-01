-- Active: 1713764893643@@lets-db.cvcoc6owuaxi.ap-northeast-2.rds.amazonaws.com@3306@lets-db
CREATE TABLE `Users_test` (
    `user_id` CHAR(36) NOT NULL, `mail` varchar(50) NOT NULL, `name` varchar(20) NOT NULL, `gender` TINYINT NOT NULL, `birthyear` CHAR(4) NOT NULL, `birthday` CHAR(4) NOT NULL, `region` varchar(10) DEFAULT NULL, `alarm` tinyint NOT NULL, `join_date` datetime NOT NULL, PRIMARY KEY (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `Login_test` (
    `token` CHAR(27) NOT NULL, `provider` varchar(10) NOT NULL, `create_time` datetime NOT NULL, PRIMARY KEY (`token`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

SELECT * FROM `Users_test`;