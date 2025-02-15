CREATE DATABASE `bronze_db`;
CREATE DATABASE `silver_db`;
CREATE DATABASE `gold_turism_db`;


CREATE TABLE bronze_db.dim_containers (
  `id` int DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  `type` enum('waste','cardboard','glass','organic','plastic') DEFAULT NULL,
  `priority` enum('high','medium','low') DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `count` int DEFAULT NULL,
  `modification_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE `bronze_db.trigger_after_update_containers` AFTER UPDATE ON `containers` FOR EACH ROW BEGIN
  IF NEW.count <> OLD.count THEN
    INSERT INTO bronze_db.dim_containers (
      id, address, type, priority, latitude, count, longitude, modification_timestamp
    )
    VALUES (
      NEW.id,
      NEW.address,
      NEW.type,
      NEW.priority,
      NEW.latitude,
      NEW.count,
      NEW.longitude,
      NOW()
    );
  END IF;
END;

-- bronze_db.dim_residus_municipis definition

CREATE TABLE bronze_db.dim_residus_municipis (
  `Any` int NOT NULL,
  `Codi municipi` int DEFAULT NULL,
  `Municipi` varchar(50) DEFAULT NULL,
  `Comarca` varchar(50) DEFAULT NULL,
  `Població` int DEFAULT NULL,
  `Autocompostatge` double DEFAULT NULL,
  `Matèria orgànica` double DEFAULT NULL,
  `Poda i jardineria` double DEFAULT NULL,
  `Paper i cartró` double DEFAULT NULL,
  `Vidre` double DEFAULT NULL,
  `Envasos lleugers` double DEFAULT NULL,
  `Residus voluminosos + fusta` double DEFAULT NULL,
  `RAEE` double DEFAULT NULL,
  `Ferralla` double DEFAULT NULL,
  `Olis vegetals` double DEFAULT NULL,
  `Tèxtil` double DEFAULT NULL,
  `Runes` double DEFAULT NULL,
  `Residus en Petites Quantitats (RPQ)` double DEFAULT NULL,
  `Piles` double DEFAULT NULL,
  `Medicaments` double DEFAULT NULL,
  `Altres recollides selectives` double DEFAULT NULL,
  `Total Recollida Selectiva` double DEFAULT NULL,
  `R.S. / R.M. % total` double DEFAULT NULL,
  `Kg/hab/any recollida selectiva` double DEFAULT NULL,
  `Resta a Dipòsit` double DEFAULT NULL,
  `Resta a Incineració` double DEFAULT NULL,
  `Resta a Tractament Mecànic Biològic` double DEFAULT NULL,
  `Resta (sense desglossar)` double DEFAULT NULL,
  `Suma Fracció Resta` double DEFAULT NULL,
  `F.R. / R.M. %` double DEFAULT NULL,
  `Generació Residus Municipal Totals` double DEFAULT NULL,
  `Kg / hab / dia` double DEFAULT NULL,
  `Kg / hab / any` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE silver_db.dim_containers (
  `id` int DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  `type` enum('waste','cardboard','glass','organic','plastic') DEFAULT NULL,
  `priority` enum('high','medium','low') DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `count` int DEFAULT NULL,
  `modification_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE silver_db.dim_residus_municipis (
  `Any` int NOT NULL,
  `Codi municipi` int DEFAULT NULL,
  `Municipi` varchar(50) DEFAULT NULL,
  `Comarca` varchar(50) DEFAULT NULL,
  `Població` int DEFAULT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




CREATE TABLE gold_db.containers (
  `id` int DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  `type` enum('waste','cardboard','glass','organic','plastic') DEFAULT NULL,
  `priority` enum('high','medium','low') DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `count` int DEFAULT NULL,
  `modification_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE gold_db.residus_municipis (
  `Any` int NOT NULL,
  `Codi municipi` int DEFAULT NULL,
  `Municipi` varchar(50) DEFAULT NULL,
  `Comarca` varchar(50) DEFAULT NULL,
  `Població` int DEFAULT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



 CREATE PROCEDURE `bronze_db`.`sp_clean_bronze_to_silver`()
BEGIN
    -- Insertamos en silver_db.containers_silver solo las filas de bronze_db.containers_bronze
    -- que no tengan ningún valor nulo.
    INSERT INTO silver_db.containers(id, address, `type`, priority, latitude, count, longitude, modification_timestamp)
    SELECT id, address, `type`, priority, latitude, count, longitude, modification_timestamp
    FROM bronze_db.dim_containers
    WHERE address IS NOT NULL
      AND `type` IS NOT NULL
      AND priority IS NOT NULL
      AND latitude IS NOT NULL
      AND count IS NOT NULL
      AND longitude IS NOT NULL
      AND modification_timestamp IS NOT NULL;
	
    
    INSERT INTO silver_db.residus_municipals (`Any`,	`Codi municipi`,	Municipi, Comarca,	`Població`)
    SELECT `Any`,	`Codi municipi`,	Municipi, Comarca,	`Població`
    FROM bronze_db.dim_residus_municipis
    WHERE `Any` IS NOT NULL
      AND `Codi municipi` IS NOT NULL
      AND Municipi IS NOT NULL
      AND `Població` IS NOT NULL;
	
END;

CREATE EVENT bronze_db.ev_weekly_clean_bronze
ON SCHEDULE EVERY 1 WEEK
STARTS '2025-02-10 00:00:00.000'
ON COMPLETION NOT PRESERVE
ENABLE
DO CALL sp_clean_bronze_to_silver();



CREATE PROCEDURE `silver_db`.`gold_eda`()
BEGIN
    -- Insertamos en silver_db.containers_silver solo las filas de bronze_db.containers_bronze
    -- que no tengan ningún valor nulo.
    INSERT INTO gold_turism_db.containers(id, `type`, priority, latitude, count, longitude, modification_timestamp)
    SELECT id, `type`, priority, latitude, count, longitude, modification_timestamp
    FROM silver_db.dim_containers;
	
    
    INSERT INTO gold_turism_db.residus_municipals (`Any`,	`Codi municipi`,	Municipi, Comarca,	`Població`)
    SELECT `Any`,	`Codi municipi`,	Municipi, Comarca,	`Població`
    FROM silver_db.dim_residus_municipis;
	
END;


CREATE EVENT silver_db.gold_eda
ON SCHEDULE EVERY 1 WEEK
STARTS '2025-02-10 00:00:00.000'
ON COMPLETION NOT PRESERVE
ENABLE
DO CALL silver_db.gold_eda();

