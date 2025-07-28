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
-- Table structure for table `retailsell`
--

DROP TABLE IF EXISTS `retailsell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retailsell` (
  `day` date NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `daytime` varchar(10) NOT NULL,
  `milk_type` varchar(20) DEFAULT NULL,
  `quantity` float NOT NULL,
  `rate` float NOT NULL,
  `amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retailsell`
--

LOCK TABLES `retailsell` WRITE;
/*!40000 ALTER TABLE `retailsell` DISABLE KEYS */;
INSERT INTO `retailsell` VALUES ('2023-04-01','Aruna Ravi Patil','morning','buffallo',1,60,60),('2023-04-02','Ujwala Hemamt Patil','morning','cow',0.5,45,22.5),('2023-04-03','Parth Ekanath Powar','evening','buffallo',1.5,60,90),('2023-04-04','vedant Hemant Patil','morning','cow',1,45,45),('2023-04-05','Vighnesh Shrikant Powar','morning','buffallo',1.5,60,90),('2023-04-06','Aradhya Ravi Patil','morning','cow',0.5,45,22.5),('2023-04-06','Aditi Hemant Patil','evening','buffallo',1.5,60,90),('2023-04-07','Sundara Gopal Patil','evening','buffallo',1,60,60),('2023-04-08','Ashwini Shivaji Patil','morning','buffallo',1.5,60,90),('2023-04-09','Aarav Ravi Patil','morning','cow',1,45,45),('2023-04-10','Abhijeet Suresh Rane','evening','cow',1.5,45,67.5),('2023-04-11','Shalan Pandurang Patil','morning','buffallo',2,60,120),('2023-04-11','Vishvajit Suresh Rane','evening','buffallo',1,60,60),('2023-04-12','Gajanan Pandurang Patil','morning','buffallo',1.5,60,90),('2023-04-13','Srushti Balarushna Chougule','morning','cow',0.5,45,22.5),('2023-04-15','Siddhi Shivaji More','evening','cow',1.5,45,67.5),('2023-04-07','Shrikant Tukaram Powar','evening','cow',1,45,45),('2023-05-09','Gayatri Ananda Patil','morning','buffallo',1,60,60);
/*!40000 ALTER TABLE `retailsell` ENABLE KEYS */;
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
