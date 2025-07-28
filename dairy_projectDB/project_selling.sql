-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `selling`
--

DROP TABLE IF EXISTS `selling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selling` (
  `day` date NOT NULL,
  `userid` int DEFAULT NULL,
  `daytime` varchar(10) NOT NULL,
  `milk_type` varchar(20) DEFAULT NULL,
  `quantity` float NOT NULL,
  `rate` float NOT NULL,
  `amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selling`
--

LOCK TABLES `selling` WRITE;
/*!40000 ALTER TABLE `selling` DISABLE KEYS */;
INSERT INTO `selling` VALUES ('2023-04-02',2,'morning','buffallo',1,60,60),('2023-04-02',2,'evening','buffallo',0.5,60,30),('2023-04-03',2,'morning','buffallo',0.5,60,30),('2023-04-03',2,'evening','buffallo',1,60,60),('2023-04-04',2,'morning','buffallo',1,60,60),('2023-04-04',2,'evening','buffallo',0.5,60,30),('2023-04-05',2,'morning','buffallo',1.5,60,90),('2023-04-06',2,'morning','buffallo',1,60,60),('2023-04-06',2,'evening','buffallo',0.5,60,30),('2023-04-07',2,'morning','buffallo',1,60,60),('2023-04-07',2,'evening','buffallo',0.5,60,30),('2023-04-08',2,'morning','buffallo',1,60,60),('2023-04-08',2,'evening','buffallo',0.5,60,30),('2023-04-09',2,'morning','buffallo',1,60,60),('2023-04-09',2,'evening','buffallo',1,60,60),('2023-04-10',2,'morning','buffallo',1.5,60,90),('2023-04-11',2,'morning','buffallo',1,60,60),('2023-04-11',2,'evening','buffallo',0.5,60,30),('2023-04-12',2,'morning','buffallo',1,60,60),('2023-04-12',2,'evening','buffallo',0.5,60,30),('2023-04-13',2,'morning','buffallo',0.5,60,30),('2023-04-13',2,'evening','buffallo',0.5,60,30),('2023-04-14',2,'morning','buffallo',1,60,60),('2023-04-14',2,'evening','buffallo',0.5,60,30),('2023-04-01',2,'morning','buffallo',1,60,60),('2023-04-15',2,'evening','buffallo',0.5,60,30),('2023-04-01',6,'morning','cow',0.5,45,22.5),('2023-04-01',8,'morning','buffallo',1,60,60),('2023-04-01',10,'evening','buffallo',1,60,60),('2023-04-01',13,'morning','buffallo',0.5,60,30),('2023-04-01',13,'evening','buffallo',0.5,60,30),('2023-04-01',15,'morning','cow',0.5,45,22.5),('2023-04-01',15,'evening','cow',0.5,45,22.5),('2023-04-01',18,'morning','cow',1,45,45),('2023-04-01',20,'morning','buffallo',1.5,60,90),('2023-04-01',20,'evening','buffallo',1,60,60),('2023-04-01',25,'morning','buffallo',1,60,60),('2023-04-01',25,'evening','buffallo',0.5,60,30),('2023-04-01',30,'morning','cow',1,45,45),('2023-04-01',32,'morning','buffallo',1.5,60,90),('2023-04-01',33,'morning','cow',1,45,45),('2023-04-01',36,'morning','buffallo',1,60,60),('2023-04-01',36,'evening','buffallo',1,60,60),('2023-04-01',38,'morning','buffallo',1,60,60),('2023-04-01',42,'evening','buffallo',1,60,60),('2023-04-02',6,'morning','buffallo',1,60,60),('2023-04-02',8,'morning','cow',1.5,45,67.5),('2023-04-02',10,'morning','buffallo',1,60,60),('2023-04-02',10,'evening','buffallo',0.5,60,30),('2023-04-02',13,'morning','cow',1,45,45),('2023-04-02',13,'evening','buffallo',0.5,60,30),('2023-04-02',15,'morning','cow',0.5,45,22.5),('2023-04-02',15,'evening','cow',0.5,45,22.5),('2023-04-02',18,'evening','buffallo',1.5,60,90),('2023-04-02',20,'morning','buffallo',1,60,60),('2023-04-02',20,'evening','cow',1,45,45),('2023-04-02',25,'morning','buffallo',1,60,60),('2023-04-02',25,'evening','buffallo',0.5,60,30),('2023-04-02',30,'morning','cow',1,45,45),('2023-04-02',30,'evening','cow',0.5,45,22.5),('2023-04-02',32,'morning','buffallo',1,60,60),('2023-04-02',32,'evening','buffallo',1,60,60),('2023-04-02',33,'morning','cow',1,45,45),('2023-04-02',36,'morning','buffallo',1,60,60),('2023-04-02',36,'evening','cow',0.5,45,22.5),('2023-04-02',38,'evening','buffallo',2,60,120),('2023-04-21',2,'morning','buffallo',1,60,60),('2023-05-09',2,'morning','buffallo',1,60,60),('2024-02-17',2,'morning','cow',1.1,45,49.5),('2024-03-06',45,'morning','buffallo',10,60,600),('2024-03-09',2,'morning','buffallo',2,60,120);
/*!40000 ALTER TABLE `selling` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-03 22:13:12
