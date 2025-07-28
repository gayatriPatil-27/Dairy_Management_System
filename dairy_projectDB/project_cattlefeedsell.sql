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
-- Table structure for table `cattlefeedsell`
--

DROP TABLE IF EXISTS `cattlefeedsell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cattlefeedsell` (
  `day` date NOT NULL,
  `userid` int NOT NULL,
  `name` varchar(30) NOT NULL,
  `feed_name` varchar(40) NOT NULL,
  `sacks` int NOT NULL,
  `rate` bigint NOT NULL,
  `amount` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cattlefeedsell`
--

LOCK TABLES `cattlefeedsell` WRITE;
/*!40000 ALTER TABLE `cattlefeedsell` DISABLE KEYS */;
INSERT INTO `cattlefeedsell` VALUES ('2023-04-02',1,'Gayatri Ananda Patil','Cotton Seed Cake',1,1350,1350),('2023-04-03',3,'shrikant Tukaram Powar','chaff',1,1000,1000),('2023-04-06',5,'Shital Ekanath Powar','Cotton Seed Goli',1,1275,1275),('2023-04-07',7,'Ekanath Tukaram Powar','chaff',1,1000,1000),('2023-04-09',9,'Bharati  Shrikant Powar','Cotton Seed Goli',1,1275,1275),('2023-04-05',11,'Sanika Shrikant Powar','Cotton Seed Goli',1,1275,1275),('2023-04-05',17,'lata ananda Patil','chaff',1,1000,1000),('2023-04-05',19,'Vidira Rajaram Vibhute','chaff',1,1000,1000),('2023-04-04',26,'Tukaram Hari Powar','Cotton Seed Goli',1,1275,1275),('2023-04-07',37,'Ritesh Maruti Ambekar','Cotton Seed Goli',1,1275,1275),('2023-04-04',41,'Shiv Sandeep Ambekar','chaff',1,1000,1000),('2023-03-16',1,'Gayatri Ananda Patil','chaff',1,1000,1000);
/*!40000 ALTER TABLE `cattlefeedsell` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-03 22:13:13
