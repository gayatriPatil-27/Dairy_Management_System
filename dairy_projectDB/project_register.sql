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
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `register` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `address` varchar(50) NOT NULL,
  `pincode` int NOT NULL,
  `phone` bigint NOT NULL,
  `cust_type` varchar(20) NOT NULL,
  `password` varchar(10) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `register`
--

LOCK TABLES `register` WRITE;
/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` VALUES (1,'gayatri','',410007,9028730295,'sell','9028'),(2,'Sayali Shrikant Powar','Kallammavadi vasahat Akiwat',416106,8806792450,'buy','8806'),(3,'shrikant Tukaram Powar','Malbhag Akiwat',416106,9850807917,'sell','9850'),(4,'Ananda Maruti Patil','A/p kalmba',416007,9423841747,'sell','9423'),(5,'Shital Ekanath Powar','Shivaji Peth Kolhapur',416001,7387097072,'sell','7387'),(6,'Mayuri Ananda Patil','A/p Kalmba',416007,7709611045,'buy','7709'),(7,'Ekanath Tukaram Powar','Kallammavadi vasahat Akiwat',416106,9420776646,'sell','9420'),(8,'Arati Ekanath Powar','Variety Block Akiwat',416106,7387115072,'buy','7387'),(9,'Bharati  Shrikant Powar','Malbhag Akiwat',416106,7517575477,'sell','7517'),(10,'Ankita Ekanath Powar','Shiwaji Peth Kolhapur',416101,9075671181,'buy','9075'),(11,'Sanika Shrikant Powar','Kallammavadi vasahat Akiwat',416106,8421262555,'sell','8421'),(12,'Shifa Ashfak Pathan','line bazar kolhapur',416006,7378880324,'sell','7378'),(13,'Samrudhi Suresh Borage','kadamwadi',416005,7385191202,'buy','7385'),(14,'Aishwarya dhanaji yadav','shivaji nagar shiroli',416122,9359232722,'sell','9359'),(15,'Apeksha Bhujgonda Patil','A/p nagav',416115,9309169086,'buy','9309'),(16,'Komal Prakash Chavan','A/p ingali',416132,9503986658,'sell','9503'),(17,'lata ananda Patil','A/p kalmba ',416007,8485806543,'sell','8485'),(18,'Shweta Bandu patil','A/p gandhinagar',416155,9765363460,'buy','9765'),(19,'Vidira Rajaram Vibhute','A/p Shahupuri kolhapur',416113,8275484718,'sell','8275'),(20,'Sanika sarjerao Shinde','Kolhapur',410100,9970803443,'buy','9970'),(21,'Piyush Maruti Ambekar','A/p Tarsambale',416211,7066102296,'sell','piya123'),(22,'Vijay Maruti Kavnekar','A/p Panori ta-shirol dist-Kolhapur',416106,7397935005,'sell','7397'),(23,'Tejas Dinakar Chougale','Malbhag A/p Akiwat ta. Shirol dist- Kolhapur',416106,9657615493,'sell','9657'),(24,'Abhishek Ragunath Powar','Kallammavadi vasahat Akiwat',416106,8308039488,'sell','8308'),(25,'Arjun Raghunath powar','Variety Block Akiwat',416106,8308478488,'buy','8308'),(26,'Tukaram Hari Powar','Kallammavadi vasahat Akiwat',416106,2322238416,'sell','02322'),(27,'Shubham Sadashiv Kavade','jain galli Akiwat ta-shirol dist-Kolhapur',416106,9146438010,'sell','9146'),(28,'Sandip namdev ambekar','shiwaji nagar Akiwat ta-shirol dist-kolhapur',416106,9112184141,'sell','9112'),(29,'Ananda Namdev Ambekar','Malbhag Akiwat',416106,9170092300,'sell','9170'),(30,'Shubham Ananda Ambekar','Kallammavadi vasahat Akiwat',416106,9689518974,'buy','9689'),(31,'laxmi Sitaram Patil','A block gurudatt sugarmill road akiwat',416106,9876543210,'sell','9876'),(32,'Sitaram Gopala Patil','Malbhag Akiwat',416106,9359652170,'buy','9359'),(33,'Asavari Sandeep Ambekar','Gurudatt sugarmill road akiwat',416106,7038486537,'buy','7038'),(34,'Mahesh Krushnat Ambekar','Malbhag Akiwat',416106,8975801242,'sell','8975'),(35,'Dipak Shankar Chougule','jain galli Akiwat ta-shirol dist-Kolhapur',416106,9049075493,'sell','9049'),(36,'Sangram Krushnat Ambekar','Malbhag Akiwat',416106,9561996970,'buy','9561'),(37,'Ritesh Maruti Ambekar','Variety Block Akiwat',416106,8459325868,'sell','8459'),(38,'Varsha Rajgonda Patil','near jain basti Akiwat',416106,8855857512,'buy','8855'),(39,'Shital Uttam Patil','a/p takali ta-shirol dist-kolhapur',416106,7259306249,'sell','7259'),(40,'Akshata Ashok Gaykwad','A/p Akiwat ta-Shirol dist-kolhapur',416106,8080216370,'sell','8080'),(41,'Shiv Sandeep Ambekar','plot no-12 guruddat road Akiwat',416106,8421226999,'sell','8421'),(42,'Sakshi Mohan Kamte','akiwat ta-Shirol dist-kolhapur',416106,8208748246,'buy','8208'),(43,'Vaishnavi prakash jadhav','near siddheshwar temple akiwat',416106,7038701560,'sell','7038'),(44,'Arati Sachin Pande','a/p akiwat ',416106,9168891661,'sell','9168'),(45,'malikjan nadaf','kadmwadi kolhapur',416006,9822959011,'buy','9822'),(46,'Gayatri Ananda Patil','A/P kalamba kolhapur',416007,2314567832,'sell','2314');
/*!40000 ALTER TABLE `register` ENABLE KEYS */;
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
