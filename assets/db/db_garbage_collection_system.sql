CREATE DATABASE `db_garbage_collection_system`;

-- db_garbage_collection_system.containers definition

CREATE TABLE db_garbage_collection_system.containers (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `type` enum('waste','cardboard','glass','organic','plastic') NOT NULL,
  `priority` enum('high','medium','low') DEFAULT NULL,
  `latitude` varchar(255) NOT NULL,
  `longitude` varchar(255) NOT NULL,
  `count` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=442 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- db_garbage_collection_system.dumpster definition

CREATE TABLE db_garbage_collection_system.dumpster (
  `id` int NOT NULL AUTO_INCREMENT,
  `latitude` varchar(255) NOT NULL,
  `longitude` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- db_garbage_collection_system.truck definition

CREATE TABLE db_garbage_collection_system.truck (
  `id` int NOT NULL AUTO_INCREMENT,
  `warehouse` int NOT NULL,
  `max_load` decimal(10,0) NOT NULL,
  `max_speed` int NOT NULL,
  `type` enum('waste','cardboard','glass','organic','plastic') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;