-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: hrms
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `assigned_det`
--

DROP TABLE IF EXISTS `assigned_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assigned_det` (
  `army_number` varchar(15) NOT NULL,
  `det_id` int DEFAULT NULL,
  `assigned_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `det_removed_date` datetime DEFAULT NULL,
  `det_status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`army_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assigned_det`
--

LOCK TABLES `assigned_det` WRITE;
/*!40000 ALTER TABLE `assigned_det` DISABLE KEYS */;
INSERT INTO `assigned_det` VALUES ('15719951L',1,'2026-02-11 16:56:58','2026-02-11 20:35:24',0),('15731820M',1,'2026-02-05 09:01:31','2026-02-05 12:37:38',0),('15740970K',2,'2025-10-11 09:49:15',NULL,1),('15753860N',1,'2026-02-05 08:53:20','2026-02-05 09:05:33',0),('A4203413X',2,'2026-02-03 09:50:08',NULL,1);
/*!40000 ALTER TABLE `assigned_det` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assigned_personnel`
--

DROP TABLE IF EXISTS `assigned_personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assigned_personnel` (
  `army_number` varchar(15) NOT NULL,
  `det_id` int DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`army_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assigned_personnel`
--

LOCK TABLES `assigned_personnel` WRITE;
/*!40000 ALTER TABLE `assigned_personnel` DISABLE KEYS */;
/*!40000 ALTER TABLE `assigned_personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assistant_test`
--

DROP TABLE IF EXISTS `assistant_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assistant_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `batch` varchar(45) NOT NULL,
  `asst_test1` datetime DEFAULT NULL,
  `asst_test2` datetime DEFAULT NULL,
  `asst_test3` datetime DEFAULT NULL,
  `asst_test4` datetime DEFAULT NULL,
  `test1_status` tinyint(1) DEFAULT '0',
  `test2_status` tinyint(1) DEFAULT '0',
  `test3_status` tinyint(1) DEFAULT '0',
  `test4_status` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `DOE` date DEFAULT NULL,
  `TOE` date DEFAULT NULL,
  `TOS` date DEFAULT NULL,
  `END_OF_TENURE` varchar(50) DEFAULT NULL,
  `emergency_test1` date DEFAULT NULL,
  `emergency_test2` date DEFAULT NULL,
  `emergency_test3` date DEFAULT NULL,
  `emergency_test4` date DEFAULT NULL,
  `emergency_test1_type` varchar(20) DEFAULT NULL,
  `emergency_test2_type` varchar(20) DEFAULT NULL,
  `emergency_test3_type` varchar(20) DEFAULT NULL,
  `emergency_test4_type` varchar(20) DEFAULT NULL,
  `str` int DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assistant_test`
--

LOCK TABLES `assistant_test` WRITE;
/*!40000 ALTER TABLE `assistant_test` DISABLE KEYS */;
INSERT INTO `assistant_test` VALUES (1,'Batch 3','2024-10-23 00:00:00','2025-04-23 00:00:00','2026-04-23 00:00:00','2027-04-23 00:00:00',1,1,0,0,'2026-01-30 13:17:53','2023-10-23','2027-10-23','2024-06-04','2026-2-4',NULL,NULL,'2028-02-21','2026-07-25',NULL,NULL,'postpone','postpone',NULL,'TEST-4 : EXAMS ARE POST PHONE DUE TO  HIGH TEMPERATURE | TEST-3 : SNOW'),(2,'Batch 1','2023-12-25 00:00:00','2024-06-25 00:00:00','2025-06-25 00:00:00','2026-06-25 00:00:00',0,1,0,0,'2026-01-30 13:18:37','2022-12-25','2026-12-25','2025-04-13','2026-12-13',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'Batch 2','2024-02-25 00:00:00','2024-08-25 00:00:00','2025-08-25 00:00:00','2026-08-25 00:00:00',1,0,0,1,'2026-01-30 13:18:44','2023-02-25','2027-02-25','2025-08-25','2027-4-25',NULL,NULL,NULL,'2026-06-26',NULL,NULL,NULL,'prepone',NULL,'DUE TO HEAVY SNOW FALL'),(4,'Batch 4','2025-04-24 00:00:00','2025-10-24 00:00:00','2026-10-24 00:00:00','2027-10-24 00:00:00',1,1,1,0,'2026-01-30 13:18:52','2024-04-24','2028-04-24','2024-12-05','2026-8-5',NULL,NULL,NULL,'2026-05-30',NULL,NULL,NULL,'postpone',NULL,'TEST-4 : THERE EXAM WILL BE IN JUNE | TEST-4 : No Remarks'),(5,'Batch 6','2026-04-25 00:00:00','2026-10-25 00:00:00','2027-10-25 00:00:00','2028-10-25 00:00:00',0,0,0,0,'2026-01-30 13:19:20','2025-04-25','2029-04-25','2025-12-05','2027-8-5',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `assistant_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_members`
--

DROP TABLE IF EXISTS `board_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) DEFAULT NULL,
  `member_name` varchar(255) DEFAULT NULL,
  `army_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_members`
--

LOCK TABLES `board_members` WRITE;
/*!40000 ALTER TABLE `board_members` DISABLE KEYS */;
INSERT INTO `board_members` VALUES (6,'123456','SHUKLA','15744564F'),(7,'123456','SHUKLA','15744564F'),(8,'4576','NB SUB H R GURJAR','JC 393919L');
/*!40000 ALTER TABLE `board_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boards`
--

DROP TABLE IF EXISTS `boards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) DEFAULT NULL,
  `entry_date` date DEFAULT NULL,
  `authority` varchar(255) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `presiding_officer` varchar(255) DEFAULT NULL,
  `completion_date` date DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boards`
--

LOCK TABLES `boards` WRITE;
/*!40000 ALTER TABLE `boards` DISABLE KEYS */;
INSERT INTO `boards` VALUES (4,'123456','2026-02-20','TEMP','center petrol checking ','PRATEEK','2026-02-26',''),(5,'4576','2026-02-07','Stn Hq letter no 123456gdf','VEH CHECKING','MAJ KISHAN','2026-02-13','');
/*!40000 ALTER TABLE `boards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_on_courses`
--

DROP TABLE IF EXISTS `candidate_on_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidate_on_courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(50) NOT NULL,
  `course_starting_date` date NOT NULL,
  `course_end_date` date NOT NULL,
  `course_name` varchar(150) NOT NULL,
  `institute_name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_courses_army_number` (`army_number`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_on_courses`
--

LOCK TABLES `candidate_on_courses` WRITE;
/*!40000 ALTER TABLE `candidate_on_courses` DISABLE KEYS */;
INSERT INTO `candidate_on_courses` VALUES (6,'15720341L','2026-02-07','2026-04-18','ttc','1ttr'),(7,'A4204811L','2026-02-14','2026-02-22','CL 2','TTR 4'),(8,'15718811m','2026-04-18','2026-07-04','S COURSE','1 MTR');
/*!40000 ALTER TABLE `candidate_on_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children`
--

DROP TABLE IF EXISTS `children`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `class` varchar(100) DEFAULT NULL,
  `part_ii_order` varchar(100) DEFAULT NULL,
  `uid_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_children` (`personnel_id`),
  CONSTRAINT `children_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children`
--

LOCK TABLES `children` WRITE;
/*!40000 ALTER TABLE `children` DISABLE KEYS */;
INSERT INTO `children` VALUES (50,66,'15689681K',1,'NAILEK PANDEY','2009-12-15','11th','0/0125/0035/2010','51382241729'),(51,66,'15689681K',2,'ANIKET PANDEY','2015-08-21','5th','0/0022/0003/2016','30944875223'),(57,64,'15719460P',1,'DEVA DARSHIKA A','2020-06-29','LKG','0/0507/0002/2020','979658721072'),(58,64,'15719460P',2,'DEVADAKSHITH A ','2022-10-05','-','0/0001/0003/2023',''),(65,40,'15720341L',1,'S HASHMITHA','2021-10-01','LKG','0/0014/0001/2002',''),(66,40,'15720341L',2,'VISHRUTHI','2025-03-06','','0/0159/0001/2025',''),(72,42,'15736949K',1,'KIRITI KUMARI','2017-10-13','1','',''),(73,42,'15736949K',2,'ANURAG KUMAR','2021-04-30','LKG','',''),(74,45,'15740970K',1,'DIVYANSH YADAV','2020-12-15','NUR','0/0036/0001/281',''),(75,60,'15731634W',1,'SHIVANSH KUMAR TIWARI','2018-03-27','2nd','0/0141/0016/2024','331099651071'),(76,60,'15731634W',2,'VEDANSH TIWARI','2021-06-26','NUS','0/0141/0022/2024','640347147190');
/*!40000 ALTER TABLE `children` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `course` varchar(255) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `institute` varchar(255) DEFAULT NULL,
  `grading` varchar(100) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_courses` (`personnel_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (51,66,'15689681K',1,'CL-I','2015-02-01','2015-05-31','3TTR','B',''),(54,64,'15719460P',1,'CL-I','2018-02-18','2018-07-25','','B',''),(58,40,'15720341L',1,'CL-1','2022-05-01','2022-12-12','','C',''),(62,42,'15736949K',1,'CL-2','2021-08-25','2022-03-21','4TTR','C',''),(63,57,'15740527W',1,'CL-2','2021-12-10','2022-08-10','','C',''),(64,57,'15740527W',2,'MR-II','2024-01-01','2024-10-28','','-',''),(65,60,'15731634W',1,'CL-I','2023-02-20','2023-05-06','2TTR','B',''),(66,60,'15731634W',2,'MR-II','2024-04-06','2024-05-25','33 ADSR','B',''),(67,133,'12345t',1,'MR1','2025-10-01','2026-03-06','SBI ','20000','GOOD'),(68,135,'12345EE',1,'MR1','2025-10-01','2026-03-06','SBI ','20000','GOOD');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_events`
--

DROP TABLE IF EXISTS `daily_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_date` date DEFAULT NULL,
  `event_name` varchar(255) DEFAULT NULL,
  `venue` varchar(255) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `company` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_events`
--

LOCK TABLES `daily_events` WRITE;
/*!40000 ALTER TABLE `daily_events` DISABLE KEYS */;
INSERT INTO `daily_events` VALUES (10,'2026-01-23','GAMEP','PT','2026-01-23 22:42:22',NULL),(11,'2026-01-31','VISIT','ALL UNIT','2026-01-31 06:42:50',NULL),(17,'2026-02-04','CELEBRATION','PT GROUND','2026-02-03 15:14:22','1 company'),(18,'2026-02-04','DANCING','ALL UNIT','2026-02-03 15:22:02',''),(19,'2026-02-05','DANCING','PT GROUND','2026-02-03 15:29:57',NULL),(22,'2026-02-13','GAME','BADMINTAN','2026-02-13 09:18:33','Admin');
/*!40000 ALTER TABLE `daily_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department_accounts`
--

DROP TABLE IF EXISTS `department_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_holder` varchar(100) NOT NULL,
  `current_balance` decimal(15,2) NOT NULL DEFAULT '0.00',
  `status` enum('ACTIVE','INACTIVE') DEFAULT 'ACTIVE',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_holder` (`account_holder`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department_accounts`
--

LOCK TABLES `department_accounts` WRITE;
/*!40000 ALTER TABLE `department_accounts` DISABLE KEYS */;
INSERT INTO `department_accounts` VALUES (11,'ATG',10000.00,'ACTIVE','2026-01-24 05:47:04','2026-01-24 05:48:51');
/*!40000 ALTER TABLE `department_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department_transactions`
--

DROP TABLE IF EXISTS `department_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `department_account_id` int NOT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `old_balance` decimal(15,2) NOT NULL,
  `credit_amount` decimal(15,2) DEFAULT '0.00',
  `debit_amount` decimal(15,2) DEFAULT '0.00',
  `new_balance` decimal(15,2) NOT NULL,
  `transaction_type` enum('CREDIT','DEBIT') NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `department_account_id` (`department_account_id`),
  CONSTRAINT `department_transactions_ibfk_1` FOREIGN KEY (`department_account_id`) REFERENCES `department_accounts` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department_transactions`
--

LOCK TABLES `department_transactions` WRITE;
/*!40000 ALTER TABLE `department_transactions` DISABLE KEYS */;
INSERT INTO `department_transactions` VALUES (12,11,'2026-01-24 11:17:53',10000.00,100.00,0.00,10100.00,'CREDIT','','2026-01-24 05:47:53'),(13,11,'2026-01-24 11:18:52',10100.00,0.00,100.00,10000.00,'CREDIT','for trg','2026-01-24 05:48:52');
/*!40000 ALTER TABLE `department_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detailed_courses`
--

DROP TABLE IF EXISTS `detailed_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detailed_courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_detailed_courses` (`personnel_id`),
  CONSTRAINT `detailed_courses_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detailed_courses`
--

LOCK TABLES `detailed_courses` WRITE;
/*!40000 ALTER TABLE `detailed_courses` DISABLE KEYS */;
/*!40000 ALTER TABLE `detailed_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dets`
--

DROP TABLE IF EXISTS `dets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dets` (
  `det_id` int NOT NULL AUTO_INCREMENT,
  `det_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`det_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dets`
--

LOCK TABLES `dets` WRITE;
/*!40000 ALTER TABLE `dets` DISABLE KEYS */;
INSERT INTO `dets` VALUES (1,'SONAMARG'),(2,'SINGHPURA'),(3,'TREHGAM'),(4,'ROSHAN'),(5,'KHREW'),(6,'SONARWEIN'),(7,'UPLONA'),(8,'MANASBAL'),(9,'KHUNMDH'),(10,'LYNGET'),(11,'TRAGBAL'),(12,'WUSAN'),(13,NULL);
/*!40000 ALTER TABLE `dets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `family_members`
--

DROP TABLE IF EXISTS `family_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `family_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `relation` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `uid_no` varchar(50) DEFAULT NULL,
  `part_ii_order` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_family` (`personnel_id`),
  CONSTRAINT `family_members_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `family_members`
--

LOCK TABLES `family_members` WRITE;
/*!40000 ALTER TABLE `family_members` DISABLE KEYS */;
INSERT INTO `family_members` VALUES (84,92,'A4201316F','FATHER','MURALEEDHARAN PILLAI','1967-05-25','496255312812',''),(85,92,'A4201316F','MOTHER','SINDHUR','1975-05-23','251545045465',''),(88,93,'A4204643X','FATHER','SUNIL','1981-01-16','698383889647',''),(89,93,'A4204643X','MOTHER','JOYTI','1982-01-01','874938924932',''),(94,64,'15719460P','FATHER','SEKHARAN NAIR G','1946-02-22','544916942456','0/0439/0024/2023'),(95,64,'15719460P','MOTHER','SREEKALA DEVI T','1962-05-31','647059138886','0/0439/0023/2023'),(96,121,'A4205888A','FATHER','RAMAJOR','1973-08-10','',''),(97,121,'A4205888A','MOTHER','ANEETA','1979-01-01','',''),(98,123,'A4206051M','FATHER','SARAVANAN P','1976-04-07','',''),(99,123,'A4206051M','MOTHER','KANDEEPAN S','1999-06-16','',''),(106,40,'15720341L','FATHER','A GURUSANY','1967-03-11','',''),(107,40,'15720341L','MOTHER','G INDIRAN','1970-02-17','',''),(114,42,'15736949K','FATHER','BHARAT YADAV','1963-01-01','746064346150',''),(115,42,'15736949K','MOTHER','BINA DEVI','1966-01-01','519120044487',''),(116,45,'15740970K','FATHER','PRAHALAD YADAV','1969-07-01','',''),(117,45,'15740970K','MOTHER','BINDOO DEVI','1973-02-20','',''),(125,56,'A4351981P','FATHER','VINOS SINGH','1971-07-01','',''),(126,51,'A4204811L','FATHER','RAMPOOT SINGH','1978-01-01','972633307819',''),(127,51,'A4204811L','MOTHER','ANJU DEVI','1981-01-01','908919155782',''),(128,57,'15740527W','FATHER','VASISHTH TIWARI','1996-12-28','',''),(129,57,'15740527W','MOTHER','BITAN DEVI','1970-02-13','',''),(130,60,'15731634W','FATHER','ASHOK KUMAR TIWARI','1965-03-15','',''),(131,60,'15731634W','MOTHER','SARASWATI TIWARI','1967-07-01','',''),(132,71,'A4354369W','FATHER','KUMAR RAVSAHE B MANE','1978-06-01','930085262147',''),(133,71,'A4354369W','MOTHER','ANITA KUMAR MANE','1981-12-11','464470383840','');
/*!40000 ALTER TABLE `family_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gallery_settings`
--

DROP TABLE IF EXISTS `gallery_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gallery_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `subtitle` text,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gallery_settings`
--

LOCK TABLES `gallery_settings` WRITE;
/*!40000 ALTER TABLE `gallery_settings` DISABLE KEYS */;
INSERT INTO `gallery_settings` VALUES (1,'SADAIV SATRAK','TEEVRA CHAUKAS','1770719417_a.jpeg'),(2,'RARE ONES','HAR MAIDAN FATEH','1770723851_chinar.jpg'),(3,'RARE ONES','KAR HAR MAIDAN FATEH','1770802562_Screenshot_2026-02-11_150445.png'),(4,'','','1771124799_image3.jpeg'),(5,'','','1771124808_signal.jpg'),(6,'RARE ONE','HAR MAIDAN FATEH','1771124907_image3.jpeg'),(7,'RARE ONES','HAR MAIDAN FATEH','1771337276_images.png');
/*!40000 ALTER TABLE `gallery_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ideal_weights`
--

DROP TABLE IF EXISTS `ideal_weights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ideal_weights` (
  `id` int NOT NULL AUTO_INCREMENT,
  `height_cm` int NOT NULL,
  `age_range` varchar(20) NOT NULL,
  `ideal_weight_kg` decimal(5,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ideal_weights`
--

LOCK TABLES `ideal_weights` WRITE;
/*!40000 ALTER TABLE `ideal_weights` DISABLE KEYS */;
INSERT INTO `ideal_weights` VALUES (2,156,'18-22',49.00,'2025-09-22 10:02:56'),(3,156,'23-27',51.00,'2025-09-22 10:02:56'),(4,156,'28-32',52.50,'2025-09-22 10:02:56'),(5,156,'33-37',53.50,'2025-09-22 10:02:56'),(6,156,'38-42',54.00,'2025-09-22 10:02:56'),(7,156,'43-47',54.50,'2025-09-22 10:02:56'),(8,156,'48-70',55.00,'2025-09-22 10:02:56'),(10,158,'18-22',50.00,'2025-09-22 10:02:56'),(11,158,'23-27',52.00,'2025-09-22 10:02:56'),(12,158,'28-32',54.00,'2025-09-22 10:02:56'),(13,158,'33-37',55.00,'2025-09-22 10:02:56'),(14,158,'38-42',55.50,'2025-09-22 10:02:56'),(15,158,'43-47',56.00,'2025-09-22 10:02:56'),(16,158,'48-70',56.50,'2025-09-22 10:02:56'),(18,160,'18-22',51.00,'2025-09-22 10:02:56'),(19,160,'23-27',53.00,'2025-09-22 10:02:56'),(20,160,'28-32',55.00,'2025-09-22 10:02:56'),(21,160,'33-37',56.00,'2025-09-22 10:02:56'),(22,160,'38-42',56.50,'2025-09-22 10:02:56'),(23,160,'43-47',57.00,'2025-09-22 10:02:56'),(24,160,'48-70',57.50,'2025-09-22 10:02:56'),(26,162,'18-22',52.50,'2025-09-22 10:02:56'),(27,162,'23-27',54.50,'2025-09-22 10:02:56'),(28,162,'28-32',56.00,'2025-09-22 10:02:56'),(29,162,'33-37',57.50,'2025-09-22 10:02:56'),(30,162,'38-42',58.00,'2025-09-22 10:02:56'),(31,162,'43-47',58.50,'2025-09-22 10:02:56'),(32,162,'48-70',59.00,'2025-09-22 10:02:56'),(34,164,'18-22',53.50,'2025-09-22 10:02:56'),(35,164,'23-27',55.50,'2025-09-22 10:02:56'),(36,164,'28-32',57.50,'2025-09-22 10:02:56'),(37,164,'33-37',59.00,'2025-09-22 10:02:56'),(38,164,'38-42',59.50,'2025-09-22 10:02:56'),(39,164,'43-47',60.00,'2025-09-22 10:02:56'),(40,164,'48-70',60.50,'2025-09-22 10:02:56'),(42,166,'18-22',55.00,'2025-09-22 10:02:56'),(43,166,'23-27',57.00,'2025-09-22 10:02:56'),(44,166,'28-32',59.00,'2025-09-22 10:02:56'),(45,166,'33-37',60.50,'2025-09-22 10:02:56'),(46,166,'38-42',61.00,'2025-09-22 10:02:56'),(47,166,'43-47',61.50,'2025-09-22 10:02:56'),(48,166,'48-70',62.00,'2025-09-22 10:02:56'),(50,168,'18-22',56.50,'2025-09-22 10:02:56'),(51,168,'23-27',58.50,'2025-09-22 10:02:56'),(52,168,'28-32',60.50,'2025-09-22 10:02:56'),(53,168,'33-37',62.00,'2025-09-22 10:02:56'),(54,168,'38-42',63.00,'2025-09-22 10:02:56'),(55,168,'43-47',63.50,'2025-09-22 10:02:56'),(56,168,'48-70',64.00,'2025-09-22 10:02:56'),(58,170,'18-22',58.00,'2025-09-22 10:02:56'),(59,170,'23-27',60.00,'2025-09-22 10:02:56'),(60,170,'28-32',62.00,'2025-09-22 10:02:56'),(61,170,'33-37',64.00,'2025-09-22 10:02:56'),(62,170,'38-42',64.50,'2025-09-22 10:02:56'),(63,170,'43-47',65.00,'2025-09-22 10:02:56'),(64,170,'48-70',65.50,'2025-09-22 10:02:56'),(66,172,'18-22',60.00,'2025-09-22 10:02:56'),(67,172,'23-27',61.50,'2025-09-22 10:02:56'),(68,172,'28-32',63.50,'2025-09-22 10:02:56'),(69,172,'33-37',65.50,'2025-09-22 10:02:56'),(70,172,'38-42',66.00,'2025-09-22 10:02:56'),(71,172,'43-47',66.50,'2025-09-22 10:02:56'),(72,172,'48-70',67.50,'2025-09-22 10:02:56'),(74,174,'18-22',61.00,'2025-09-22 10:02:56'),(75,174,'23-27',63.50,'2025-09-22 10:02:56'),(76,174,'28-32',65.50,'2025-09-22 10:02:56'),(77,174,'33-37',67.50,'2025-09-22 10:02:56'),(78,174,'38-42',68.00,'2025-09-22 10:02:56'),(79,174,'43-47',68.50,'2025-09-22 10:02:56'),(80,174,'48-70',69.00,'2025-09-22 10:02:56'),(82,176,'18-22',62.50,'2025-09-22 10:02:56'),(83,176,'23-27',65.00,'2025-09-22 10:02:56'),(84,176,'28-32',67.00,'2025-09-22 10:02:56'),(85,176,'33-37',69.00,'2025-09-22 10:02:56'),(86,176,'38-42',69.50,'2025-09-22 10:02:56'),(87,176,'43-47',70.00,'2025-09-22 10:02:56'),(88,176,'48-70',71.00,'2025-09-22 10:02:56'),(90,178,'18-22',64.00,'2025-09-22 10:02:56'),(91,178,'23-27',66.50,'2025-09-22 10:02:56'),(92,178,'28-32',68.50,'2025-09-22 10:02:56'),(93,178,'33-37',70.50,'2025-09-22 10:02:56'),(94,178,'38-42',71.50,'2025-09-22 10:02:56'),(95,178,'43-47',72.00,'2025-09-22 10:02:56'),(96,178,'48-70',72.50,'2025-09-22 10:02:56'),(98,180,'18-22',65.50,'2025-09-22 10:02:56'),(99,180,'23-27',68.00,'2025-09-22 10:02:56'),(100,180,'28-32',70.50,'2025-09-22 10:02:56'),(101,180,'33-37',72.50,'2025-09-22 10:02:56'),(102,180,'38-42',73.00,'2025-09-22 10:02:56'),(103,180,'43-47',74.00,'2025-09-22 10:02:56'),(104,180,'48-70',74.50,'2025-09-22 10:02:56'),(106,182,'18-22',67.50,'2025-09-22 10:02:56'),(107,182,'23-27',69.50,'2025-09-22 10:02:56'),(108,182,'28-32',72.00,'2025-09-22 10:02:56'),(109,182,'33-37',74.00,'2025-09-22 10:02:56'),(110,182,'38-42',75.00,'2025-09-22 10:02:56'),(111,182,'43-47',75.50,'2025-09-22 10:02:56'),(112,182,'48-70',76.50,'2025-09-22 10:02:56'),(114,184,'18-22',70.00,'2025-09-22 10:02:56'),(115,184,'23-27',71.50,'2025-09-22 10:02:56'),(116,184,'28-32',74.00,'2025-09-22 10:02:56'),(117,184,'33-37',76.00,'2025-09-22 10:02:56'),(118,184,'38-42',76.50,'2025-09-22 10:02:56'),(119,184,'43-47',77.50,'2025-09-22 10:02:56'),(120,184,'48-70',78.00,'2025-09-22 10:02:56'),(122,186,'18-22',70.50,'2025-09-22 10:02:56'),(123,186,'23-27',73.00,'2025-09-22 10:02:56'),(124,186,'28-32',75.50,'2025-09-22 10:02:56'),(125,186,'33-37',78.00,'2025-09-22 10:02:56'),(126,186,'38-42',78.50,'2025-09-22 10:02:56'),(127,186,'43-47',79.00,'2025-09-22 10:02:56'),(128,186,'48-70',80.00,'2025-09-22 10:02:56'),(130,188,'18-22',72.00,'2025-09-22 10:02:56'),(131,188,'23-27',75.00,'2025-09-22 10:02:56'),(132,188,'28-32',77.60,'2025-09-22 10:02:56'),(133,188,'33-37',79.50,'2025-09-22 10:02:56'),(134,188,'38-42',80.00,'2025-09-22 10:02:56'),(135,188,'43-47',81.00,'2025-09-22 10:02:56'),(136,188,'48-70',82.00,'2025-09-22 10:02:56'),(138,190,'18-22',73.50,'2025-09-22 10:02:56'),(139,190,'23-27',76.00,'2025-09-22 10:02:56'),(140,190,'28-32',78.50,'2025-09-22 10:02:56'),(141,190,'33-37',80.50,'2025-09-22 10:02:56'),(142,190,'38-42',81.00,'2025-09-22 10:02:56'),(143,190,'43-47',82.00,'2025-09-22 10:02:56'),(144,190,'48-70',83.00,'2025-09-22 10:02:56');
/*!40000 ALTER TABLE `ideal_weights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jco_kunda_assignment`
--

DROP TABLE IF EXISTS `jco_kunda_assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jco_kunda_assignment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(50) NOT NULL,
  `additional_assigned_home_state` varchar(100) NOT NULL,
  `interview_status` enum('Pending','Done') DEFAULT 'Pending',
  `assigned_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jco_kunda_assignment`
--

LOCK TABLES `jco_kunda_assignment` WRITE;
/*!40000 ALTER TABLE `jco_kunda_assignment` DISABLE KEYS */;
INSERT INTO `jco_kunda_assignment` VALUES (1,'jc393919L','ANDHRA PRADESH','Done','2026-02-04 07:19:00'),(2,'JC457693','ANDHRA PRADESH','Pending','2026-02-08 11:00:18'),(3,'jc393919L','KARNATAKA','Pending','2026-02-08 11:01:14'),(4,'JC457693','BIHAR','Pending','2026-02-10 06:28:08');
/*!40000 ALTER TABLE `jco_kunda_assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_details`
--

DROP TABLE IF EXISTS `leave_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `year` varchar(10) DEFAULT NULL,
  `al_days` int DEFAULT NULL,
  `cl_days` int DEFAULT NULL,
  `aal_days` int DEFAULT NULL,
  `total_days` int DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_leave` (`personnel_id`),
  CONSTRAINT `leave_details_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_details`
--

LOCK TABLES `leave_details` WRITE;
/*!40000 ALTER TABLE `leave_details` DISABLE KEYS */;
INSERT INTO `leave_details` VALUES (62,40,'15720341L',1,'2025',36,30,NULL,66,''),(69,42,'15736949K',1,'2024',28,30,NULL,58,''),(70,42,'15736949K',2,'2025',28,30,NULL,58,''),(71,51,'A4204811L',1,'2025',30,NULL,NULL,30,''),(72,135,'12345EE',1,'AIRTEL',20,20,30,40,'');
/*!40000 ALTER TABLE `leave_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_history`
--

DROP TABLE IF EXISTS `leave_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `leave_request_id` int NOT NULL,
  `army_number` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `leave_type` varchar(50) NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `total_days` int NOT NULL,
  `recommended_by` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Recommended by SEC NCO',
  `remarks` text,
  `recommended_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reject_reason` text,
  `company` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_history`
--

LOCK TABLES `leave_history` WRITE;
/*!40000 ALTER TABLE `leave_history` DISABLE KEYS */;
INSERT INTO `leave_history` VALUES (2,5,'15730189W','JITENDRA SINGH','AL','2026-01-29','2026-02-07',10,'NCO MW','Pending at JCO MW','FA,ILY','2026-01-23 22:12:27',NULL,NULL),(3,5,'15730189W','JITENDRA SINGH','AL','2026-01-29','2026-02-07',10,'jco_mw_1','Rejected at JCO MW','Leave rejected','2026-01-23 22:18:01','OW','1 company'),(4,5,'15730189W','JITENDRA SINGH','AL','2026-01-29','2026-02-07',10,'S/JCO','Pending at OC','FA,ILY','2026-01-23 22:21:04',NULL,NULL),(5,5,'15730189W','JITENDRA SINGH','AL','2026-01-29','2026-02-07',10,'RAHUL SINGH','Rejected at OC','Leave rejected','2026-01-23 22:36:57','ow','1 company'),(6,6,'A4201316F','ASWIN M','AL','2026-03-01','2026-03-18',18,'NCO IT','Pending at JCO IT','TEST','2026-01-28 06:12:59',NULL,NULL),(7,9,'15731820M','JINCE L','AL','2026-02-01','2026-02-07',7,'GHANSHYAM MAHLA','Rejected at NCO IT','Leave rejected','2026-01-31 04:20:17','OW','1 company'),(8,6,'A4201316F','ASWIN M','AL','2026-03-01','2026-03-18',18,'JCO IT','Pending at S/JCO','TEST','2026-02-01 06:10:12',NULL,NULL),(9,6,'A4201316F','ASWIN M','AL','2026-03-01','2026-03-18',18,'S/JCO','Pending at OC','TEST','2026-02-01 06:10:57',NULL,NULL),(10,6,'A4201316F','ASWIN M','AL','2026-03-01','2026-03-18',18,'OC','Approved','TEST','2026-02-01 06:11:33',NULL,NULL),(11,10,'15740527W','BRAJESH TIWARI','CL','2026-02-09','2026-02-14',6,'NCO MW','Pending at JCO MW','for family reasons','2026-02-03 09:20:12',NULL,NULL),(12,10,'15740527W','BRAJESH TIWARI','CL','2026-02-09','2026-02-14',6,'JCO MW','Pending at S/JCO','for family reasons','2026-02-03 09:22:03',NULL,NULL),(13,10,'15740527W','BRAJESH TIWARI','CL','2026-02-09','2026-02-14',6,'S/JCO','Pending at OC','for family reasons','2026-02-03 09:22:38',NULL,NULL),(14,10,'15740527W','BRAJESH TIWARI','CL','2026-02-09','2026-02-14',6,'OC','Approved','for family reasons','2026-02-03 09:23:30',NULL,NULL),(15,7,'A4203007X','Majgaonkar Rushikesh Prakash','AL','2026-02-02','2026-02-06',5,'CO','Approved','MARRIAGE','2026-02-03 12:31:56',NULL,NULL),(16,11,'15719951L','PREM MOHAN','AL','2026-02-19','2026-02-28',10,'NCO IT','Pending at JCO IT','eam','2026-02-07 12:54:11',NULL,NULL),(17,11,'15719951L','PREM MOHAN','AL','2026-02-19','2026-02-28',10,'jco_it_1','Rejected at JCO IT','Leave rejected','2026-02-07 12:56:38','ow','1 company'),(18,11,'15719951L','PREM MOHAN','AL','2026-02-19','2026-02-28',10,'jco_it_1','Rejected at JCO IT','Leave rejected','2026-02-07 13:02:02','ow','1 company'),(19,11,'15719951L','PREM MOHAN','AL','2026-02-19','2026-02-28',10,'S/JCO','Pending at OC','eam','2026-02-07 13:07:46',NULL,NULL),(20,11,'15719951L','PREM MOHAN','AL','2026-02-19','2026-02-28',10,'PRATEEK','Rejected at OC','Leave rejected','2026-02-07 13:08:39','due to over weight','1 company'),(21,11,'15719951L','PREM MOHAN','AL','2026-02-19','2026-02-28',10,'CO','Approved','eam','2026-02-07 13:55:54',NULL,NULL),(22,5,'15730189W','JITENDRA SINGH','AL','2026-01-29','2026-02-07',10,'CO','Approved','FA,ILY','2026-02-11 08:24:47',NULL,NULL);
/*!40000 ALTER TABLE `leave_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_status_info`
--

DROP TABLE IF EXISTS `leave_status_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_status_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(50) NOT NULL,
  `name` varchar(45) NOT NULL,
  `leave_type` varchar(50) NOT NULL,
  `leave_days` int NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `request_sent_to` varchar(150) DEFAULT NULL,
  `request_status` varchar(50) DEFAULT 'Pending',
  `recommend_date` datetime DEFAULT NULL,
  `rejected_date` datetime DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `leave_reason` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `reject_reason` text,
  `company` varchar(50) DEFAULT NULL,
  `prefix_date` date DEFAULT NULL,
  `suffix_date` date DEFAULT NULL,
  `prefix_days` int DEFAULT '0',
  `suffix_days` int DEFAULT '0',
  `rank` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_status_info`
--

LOCK TABLES `leave_status_info` WRITE;
/*!40000 ALTER TABLE `leave_status_info` DISABLE KEYS */;
INSERT INTO `leave_status_info` VALUES (5,'15730189W','JITENDRA SINGH','AL',10,'2026-01-29','2026-02-07','','Approved','2026-02-11 13:54:47',NULL,'AL for 10 day(s)','FA,ILY','2026-01-24 03:39:02','2026-02-11 13:54:47','ow','1 company',NULL,NULL,0,0,NULL),(6,'A4201316F','ASWIN M','AL',18,'2026-03-01','2026-03-18','','Approved','2026-02-01 11:41:33',NULL,'AL for 20 day(s) (Actual: 18 days)','TEST','2026-01-28 11:39:07','2026-02-01 11:41:33',NULL,'1 company',NULL,NULL,0,0,NULL),(7,'A4203007X','Majgaonkar Rushikesh Prakash','AL',5,'2026-02-02','2026-02-06','','Approved','2026-02-03 18:01:56',NULL,'AL for 6 day(s) (Actual: 5 days)','MARRIAGE','2026-01-28 12:40:10','2026-02-03 18:01:56',NULL,'1 company',NULL,NULL,0,0,NULL),(8,'A4203079F','ROSHAN KESHARWANI','AL',6,'2026-02-02','2026-02-07','NCO IT','Pending at NCO IT',NULL,NULL,'AL for 8 day(s) (Actual: 6 days)','EXAME','2026-01-31 09:07:23','2026-01-31 09:10:57',NULL,'1 company',NULL,NULL,0,0,NULL),(9,'15731820M','JINCE L','AL',7,'2026-02-01','2026-02-07','NCO IT','Rejected at NCO IT',NULL,'2026-01-31 09:50:17','AL for 9 day(s) (Actual: 7 days)','TEMPLE VISIT','2026-01-31 09:48:04','2026-01-31 09:50:17','OW','1 company',NULL,NULL,0,0,NULL),(10,'15740527W','BRAJESH TIWARI','CL',6,'2026-02-09','2026-02-14','','Approved','2026-02-03 14:53:30',NULL,'CL for 8 day(s) (Actual: 6 days)','for family reasons','2026-02-03 14:48:20','2026-02-03 15:20:36',NULL,'1 company','2026-02-08','2026-02-15',0,0,NULL),(11,'15719951L','PREM MOHAN','AL',10,'2026-02-19','2026-02-28','','Approved','2026-02-07 19:25:54',NULL,'AL for 10 day(s) (Actual: 10 days, Prefix: 0, Suffix: 0)','eam','2026-02-07 18:22:12','2026-02-07 19:25:54','due to over weight','1 company',NULL,NULL,0,0,NULL),(12,'A4203499F','PRADEEP KUMAR NAHAK','AL',6,'2026-03-02','2026-03-07','NCO CHQ','Pending at NCO CHQ',NULL,NULL,'AL for 8 day(s) (Actual: 6 days, Prefix: 1, Suffix: 1)','leave','2026-02-12 10:28:52','2026-02-12 10:28:52',NULL,'1 company','2026-03-01','2026-03-08',1,1,'Agniveer'),(13,'15753860N','MOHANRAJ T','AL',22,'2026-02-12','2026-03-05','NCO IT','Pending at NCO IT',NULL,NULL,'AL for 22 day(s) (Actual: 22 days, Prefix: 0, Suffix: 0)','MARRIAGE','2026-02-12 11:08:29','2026-02-12 11:08:29',NULL,'1 company',NULL,NULL,0,0,'NK'),(14,'15718811M','GHANSHYAM MAHLA','AL',38,'2026-01-01','2026-02-07','NCO NCO IT','Pending at NCO NCO IT',NULL,NULL,'AL for 38 day(s) (Actual: 38 days, Prefix: 0, Suffix: 0)','EXAM','2026-02-12 16:50:54','2026-02-12 16:50:54',NULL,'1 company',NULL,NULL,0,0,'HAV');
/*!40000 ALTER TABLE `leave_status_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `loan_type` varchar(255) DEFAULT NULL,
  `total_amount` decimal(15,2) DEFAULT NULL,
  `bank_details` varchar(255) DEFAULT NULL,
  `emi_per_month` decimal(15,2) DEFAULT NULL,
  `pending` decimal(15,2) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_loans` (`personnel_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (65,64,'15719460P',1,'HOME LOAN',2600000.00,'SBI',25000.00,1900000.00,''),(75,40,'15720341L',1,'HOME LOAN',1600000.00,'SBI',15000.00,1085000.00,''),(76,40,'15720341L',2,'PERSONAL LOAN',350000.00,'SBI',15000.00,217078.00,''),(80,42,'15736949K',1,'PERSONAL LOAN',130000.00,'SBI',25000.00,1070000.00,''),(81,51,'A4204811L',1,'PERSONAL LOAN',400000.00,'SBI',19200.00,NULL,''),(82,57,'15740527W',1,'PERSONAL',800000.00,'ICICI',22121.00,NULL,''),(83,57,'15740527W',2,'PERSONAL LOAN',291000.00,'PNB',5919.00,NULL,''),(84,61,'15740824K',1,'PERSONAL LOAN',210000.00,'SBI',25325.00,NULL,''),(85,60,'15731634W',1,'HOME LOAN',1469500.00,'ICICI BANK',14811.00,1356000.00,'');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marital_discord_cases`
--

DROP TABLE IF EXISTS `marital_discord_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marital_discord_cases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `case_no` varchar(100) DEFAULT NULL,
  `amount_to_pay` decimal(15,2) DEFAULT NULL,
  `sanction_letter_no` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_discord` (`personnel_id`),
  CONSTRAINT `marital_discord_cases_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marital_discord_cases`
--

LOCK TABLES `marital_discord_cases` WRITE;
/*!40000 ALTER TABLE `marital_discord_cases` DISABLE KEYS */;
/*!40000 ALTER TABLE `marital_discord_cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('sent','read') DEFAULT 'sent',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,1,5,'Hii','2026-02-10 11:49:04','read'),(2,5,1,'shaadi hui kya apki','2026-02-10 11:50:34','read'),(3,1,5,'Ha','2026-02-10 11:50:49','read'),(4,1,2,'HI how are you?','2026-02-10 11:52:20','read'),(5,1,5,'acha g aisa hai kkya','2026-02-10 13:35:29','read'),(6,1,5,'Haan g','2026-02-10 14:02:41','read'),(7,1,74,'hello','2026-02-10 14:39:43','read'),(8,1,38,'hi','2026-02-10 14:55:13','sent'),(9,74,25,'HII','2026-02-10 16:02:00','sent'),(10,41,2,'Hi','2026-02-12 11:50:21','read'),(11,2,41,'how are whats the update','2026-02-12 11:51:07','read'),(12,1,5,'hi','2026-02-17 13:25:47','read'),(13,1,5,'hi','2026-02-17 13:37:28','read'),(14,1,5,'hello world','2026-02-17 13:37:38','read'),(15,5,1,'hi','2026-02-17 14:22:46','read'),(16,1,5,'how are u','2026-02-17 14:22:55','read'),(17,5,1,'im fine and how are u','2026-02-17 14:23:01','read'),(18,1,5,'ok greate','2026-02-17 14:23:04','read'),(19,1,5,'ok bye goodnight','2026-02-17 14:23:13','read'),(20,1,5,'thank s','2026-02-17 14:24:15','read'),(21,5,1,'ok wel come tanks','2026-02-17 14:24:21','read');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mobile_phones`
--

DROP TABLE IF EXISTS `mobile_phones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mobile_phones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `number` varchar(50) DEFAULT NULL,
  `service_provider` varchar(100) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_mobiles` (`personnel_id`),
  CONSTRAINT `mobile_phones_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mobile_phones`
--

LOCK TABLES `mobile_phones` WRITE;
/*!40000 ALTER TABLE `mobile_phones` DISABLE KEYS */;
INSERT INTO `mobile_phones` VALUES (47,66,'15689681K',1,'MOTROLA ','9511058016','AIRTEL',''),(50,81,'15720596L',1,'OPPO','6204442135','JIO',''),(51,82,'A4204797K',1,'MOTOROLA','7067652835','AIRTEL',''),(52,84,'15716216K',1,'VIVO','7238984597','',''),(53,85,'15709802K',1,'INFINIX 688B','9334030074','',''),(56,88,'15731820M',1,'VIVO V21','8300797369','AIRTEL',''),(57,89,'15740143F',1,'SAMSUNG S23','8943371661','JIO',''),(58,90,'15749660A',1,'SAMSUNG S24 ULTRA','9564202863','AIRTEL',''),(59,91,'15753860N',1,'POCOF6','7373305452','AIRTEL',''),(60,92,'A4201316F',1,'REDMI 9 PRIME','8899571957','AIRTEL',''),(62,93,'A4204643X',1,'OPPO A775','7057732835','AIRTEL',''),(63,95,'A4203079F',1,'REALME 7','83570507938','JIO',''),(64,96,'A4351064L',1,'REDMI 9 PRIME','8082158339','AIRTEL',''),(65,98,'1574165Y',1,'VIVO Y28','9797623284','AIRTEL',''),(66,99,'15692903Y',1,'SAMSUNG M-14','8830886518','JIO',''),(67,100,'15720931K',1,'REALME 5 PRO','6006683105','JIO',''),(69,64,'15719460P',1,'ONE PLUS NODE ','9567212167','AIRTEL',''),(70,102,'15722524A',1,'SAMSUNG A23','6266171458','JIO',''),(71,103,'15724706M',1,'VIVO V 29E','8399803853','AIRTEL',''),(72,104,'A4203499F',1,'SAMSUNG A23','9438237465','JIO',''),(74,107,'15732973H',1,'VIVO T4X','9149679319','JIO',''),(75,108,'A4205053L',1,'I PHONE','9103811151','JIO',''),(76,109,'15748339K',1,'VIVO T2X','9471210064','AIRTEL',''),(77,110,'15736649H',1,'ONE PLUS 9R','8871312108','JIO',''),(78,111,'15721376N',1,'MOTO E40','9103113980','JIO',''),(79,113,'A4204856L',1,'RMX3612','9103705324','JIO',''),(80,114,'A4203556X',1,'POCO M3','8483048897','AIRTEL',''),(81,115,'A4205008Y',1,'REALME 8','9103921488','JIO',''),(82,116,'A4204930F',1,'SAMSUNG A21','9209086463','AIRTEL',''),(84,117,'A4205213A',1,'OPPO RENO 14','7051048039','JIO',''),(85,118,'A4200365X',1,'SAMSUNG GALAXY J6','9041103532','AIRTEL',''),(86,123,'A4206051M',1,'REALME 80X','9345824894','',''),(90,40,'15720341L',1,'OPPO','8838568774','JIO',''),(94,42,'15736949K',1,'OPPO A3','8298347320','JIO',''),(95,45,'15740970K',1,'ONE PLUS LITE','9415038851','JIO',''),(99,106,'A4207474M',1,'REALME NARZO 30A','9335797674','JIO',''),(100,124,'15715916L',1,'REALME','8464888535','AIRTEL',''),(101,125,'15742217K',1,'SAMSUNG S22','6005052132','JIO',''),(102,126,'15756017Y',1,'MOTO G 54','913998157','JIO',''),(103,127,'A4205388H',1,'OPPO F19 PRO','8899330452','AIRTEL',''),(104,128,'15752536K',1,'SAMSUNG A36','7860471110','AIRTEL',''),(105,129,'15706852K',1,'LAVA A1 VIBE','7901737951','AIRTEL',''),(106,57,'15740527W',1,'VIVO P3','9906422168','AIRTEL',''),(107,60,'15731634W',1,'MOTOROLA EDGE 50FUSION','85068900612','AIRTEL',''),(108,71,'A4354369W',1,'VIVO','9766732682','JIO',''),(109,130,'A4350867L',1,'POCO M2','8825020847','AIRTEL','');
/*!40000 ALTER TABLE `mobile_phones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monthly_medical_status`
--

DROP TABLE IF EXISTS `monthly_medical_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_medical_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL,
  `month` tinyint NOT NULL,
  `unit` varchar(50) NOT NULL,
  `unfit_count` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_year_month_unit` (`year`,`month`,`unit`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monthly_medical_status`
--

LOCK TABLES `monthly_medical_status` WRITE;
/*!40000 ALTER TABLE `monthly_medical_status` DISABLE KEYS */;
INSERT INTO `monthly_medical_status` VALUES (27,2026,1,'All',0,'2026-01-23 17:56:05'),(28,2026,1,'1 Company',0,'2026-01-23 17:56:07'),(29,2026,1,'2 Company',0,'2026-01-23 17:56:09'),(30,2026,1,'3 Company',0,'2026-01-23 17:56:11'),(31,2026,1,'HQ company',0,'2026-01-23 17:56:13'),(32,2026,2,'All',29,'2026-02-01 13:53:26'),(33,2026,2,'1 Company',29,'2026-02-01 13:53:27'),(34,2026,2,'2 Company',0,'2026-02-01 13:53:27'),(35,2026,2,'3 Company',0,'2026-02-01 13:53:27'),(36,2026,2,'HQ company',0,'2026-02-01 13:53:27');
/*!40000 ALTER TABLE `monthly_medical_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parade_state_daily`
--

DROP TABLE IF EXISTS `parade_state_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parade_state_daily` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_date` date NOT NULL,
  `company` varchar(100) NOT NULL,
  `offr_auth` int DEFAULT '0',
  `offr_hs` int DEFAULT '0',
  `offr_posted_str` int DEFAULT '0',
  `offr_lve` int DEFAULT '0',
  `offr_course` int DEFAULT '0',
  `offr_det` int DEFAULT '0',
  `offr_mh` int DEFAULT '0',
  `offr_sick_lve` int DEFAULT '0',
  `offr_ex` int DEFAULT '0',
  `offr_td` int DEFAULT '0',
  `offr_att` int DEFAULT '0',
  `offr_awl_osl_jc` int DEFAULT '0',
  `offr_trout_det` int DEFAULT '0',
  `offr_present_det` int DEFAULT '0',
  `offr_present_unit` int DEFAULT '0',
  `offr_dues_in` int DEFAULT '0',
  `offr_dues_out` int DEFAULT '0',
  `jco_auth` int DEFAULT '0',
  `jco_hs` int DEFAULT '0',
  `jco_posted_str` int DEFAULT '0',
  `jco_lve` int DEFAULT '0',
  `jco_course` int DEFAULT '0',
  `jco_det` int DEFAULT '0',
  `jco_mh` int DEFAULT '0',
  `jco_sick_lve` int DEFAULT '0',
  `jco_ex` int DEFAULT '0',
  `jco_td` int DEFAULT '0',
  `jco_att` int DEFAULT '0',
  `jco_awl_osl_jc` int DEFAULT '0',
  `jco_trout_det` int DEFAULT '0',
  `jco_present_det` int DEFAULT '0',
  `jco_present_unit` int DEFAULT '0',
  `jco_dues_in` int DEFAULT '0',
  `jco_dues_out` int DEFAULT '0',
  `jcoEre_auth` int DEFAULT '0',
  `jcoEre_hs` int DEFAULT '0',
  `jcoEre_posted_str` int DEFAULT '0',
  `jcoEre_lve` int DEFAULT '0',
  `jcoEre_course` int DEFAULT '0',
  `jcoEre_det` int DEFAULT '0',
  `jcoEre_mh` int DEFAULT '0',
  `jcoEre_sick_lve` int DEFAULT '0',
  `jcoEre_ex` int DEFAULT '0',
  `jcoEre_td` int DEFAULT '0',
  `jcoEre_att` int DEFAULT '0',
  `jcoEre_awl_osl_jc` int DEFAULT '0',
  `jcoEre_trout_det` int DEFAULT '0',
  `jcoEre_present_det` int DEFAULT '0',
  `jcoEre_present_unit` int DEFAULT '0',
  `jcoEre_dues_in` int DEFAULT '0',
  `jcoEre_dues_out` int DEFAULT '0',
  `or_auth` int DEFAULT '0',
  `or_hs` int DEFAULT '0',
  `or_posted_str` int DEFAULT '0',
  `or_lve` int DEFAULT '0',
  `or_course` int DEFAULT '0',
  `or_det` int DEFAULT '0',
  `or_mh` int DEFAULT '0',
  `or_sick_lve` int DEFAULT '0',
  `or_ex` int DEFAULT '0',
  `or_td` int DEFAULT '0',
  `or_att` int DEFAULT '0',
  `or_awl_osl_jc` int DEFAULT '0',
  `or_trout_det` int DEFAULT '0',
  `or_present_det` int DEFAULT '0',
  `or_present_unit` int DEFAULT '0',
  `or_dues_in` int DEFAULT '0',
  `or_dues_out` int DEFAULT '0',
  `orEre_auth` int DEFAULT '0',
  `orEre_hs` int DEFAULT '0',
  `orEre_posted_str` int DEFAULT '0',
  `orEre_lve` int DEFAULT '0',
  `orEre_course` int DEFAULT '0',
  `orEre_det` int DEFAULT '0',
  `orEre_mh` int DEFAULT '0',
  `orEre_sick_lve` int DEFAULT '0',
  `orEre_ex` int DEFAULT '0',
  `orEre_td` int DEFAULT '0',
  `orEre_att` int DEFAULT '0',
  `orEre_awl_osl_jc` int DEFAULT '0',
  `orEre_trout_det` int DEFAULT '0',
  `orEre_present_det` int DEFAULT '0',
  `orEre_present_unit` int DEFAULT '0',
  `orEre_dues_in` int DEFAULT '0',
  `orEre_dues_out` int DEFAULT '0',
  `firstTotal_auth` int DEFAULT '0',
  `firstTotal_hs` int DEFAULT '0',
  `firstTotal_posted_str` int DEFAULT '0',
  `firstTotal_lve` int DEFAULT '0',
  `firstTotal_course` int DEFAULT '0',
  `firstTotal_det` int DEFAULT '0',
  `firstTotal_mh` int DEFAULT '0',
  `firstTotal_sick_lve` int DEFAULT '0',
  `firstTotal_ex` int DEFAULT '0',
  `firstTotal_td` int DEFAULT '0',
  `firstTotal_att` int DEFAULT '0',
  `firstTotal_awl_osl_jc` int DEFAULT '0',
  `firstTotal_trout_det` int DEFAULT '0',
  `firstTotal_present_det` int DEFAULT '0',
  `firstTotal_present_unit` int DEFAULT '0',
  `firstTotal_dues_in` int DEFAULT '0',
  `firstTotal_dues_out` int DEFAULT '0',
  `oaOr_auth` int DEFAULT '0',
  `oaOr_hs` int DEFAULT '0',
  `oaOr_posted_str` int DEFAULT '0',
  `oaOr_lve` int DEFAULT '0',
  `oaOr_course` int DEFAULT '0',
  `oaOr_det` int DEFAULT '0',
  `oaOr_mh` int DEFAULT '0',
  `oaOr_sick_lve` int DEFAULT '0',
  `oaOr_ex` int DEFAULT '0',
  `oaOr_td` int DEFAULT '0',
  `oaOr_att` int DEFAULT '0',
  `oaOr_awl_osl_jc` int DEFAULT '0',
  `oaOr_trout_det` int DEFAULT '0',
  `oaOr_present_det` int DEFAULT '0',
  `oaOr_present_unit` int DEFAULT '0',
  `oaOr_dues_in` int DEFAULT '0',
  `oaOr_dues_out` int DEFAULT '0',
  `attSummary_auth` int DEFAULT '0',
  `attSummary_hs` int DEFAULT '0',
  `attSummary_posted_str` int DEFAULT '0',
  `attSummary_lve` int DEFAULT '0',
  `attSummary_course` int DEFAULT '0',
  `attSummary_det` int DEFAULT '0',
  `attSummary_mh` int DEFAULT '0',
  `attSummary_sick_lve` int DEFAULT '0',
  `attSummary_ex` int DEFAULT '0',
  `attSummary_td` int DEFAULT '0',
  `attSummary_att` int DEFAULT '0',
  `attSummary_awl_osl_jc` int DEFAULT '0',
  `attSummary_trout_det` int DEFAULT '0',
  `attSummary_present_det` int DEFAULT '0',
  `attSummary_present_unit` int DEFAULT '0',
  `attSummary_dues_in` int DEFAULT '0',
  `attSummary_dues_out` int DEFAULT '0',
  `attOffr_auth` int DEFAULT '0',
  `attOffr_hs` int DEFAULT '0',
  `attOffr_posted_str` int DEFAULT '0',
  `attOffr_lve` int DEFAULT '0',
  `attOffr_course` int DEFAULT '0',
  `attOffr_det` int DEFAULT '0',
  `attOffr_mh` int DEFAULT '0',
  `attOffr_sick_lve` int DEFAULT '0',
  `attOffr_ex` int DEFAULT '0',
  `attOffr_td` int DEFAULT '0',
  `attOffr_att` int DEFAULT '0',
  `attOffr_awl_osl_jc` int DEFAULT '0',
  `attOffr_trout_det` int DEFAULT '0',
  `attOffr_present_det` int DEFAULT '0',
  `attOffr_present_unit` int DEFAULT '0',
  `attOffr_dues_in` int DEFAULT '0',
  `attOffr_dues_out` int DEFAULT '0',
  `attJco_auth` int DEFAULT '0',
  `attJco_hs` int DEFAULT '0',
  `attJco_posted_str` int DEFAULT '0',
  `attJco_lve` int DEFAULT '0',
  `attJco_course` int DEFAULT '0',
  `attJco_det` int DEFAULT '0',
  `attJco_mh` int DEFAULT '0',
  `attJco_sick_lve` int DEFAULT '0',
  `attJco_ex` int DEFAULT '0',
  `attJco_td` int DEFAULT '0',
  `attJco_att` int DEFAULT '0',
  `attJco_awl_osl_jc` int DEFAULT '0',
  `attJco_trout_det` int DEFAULT '0',
  `attJco_present_det` int DEFAULT '0',
  `attJco_present_unit` int DEFAULT '0',
  `attJco_dues_in` int DEFAULT '0',
  `attJco_dues_out` int DEFAULT '0',
  `attOr_auth` int DEFAULT '0',
  `attOr_hs` int DEFAULT '0',
  `attOr_posted_str` int DEFAULT '0',
  `attOr_lve` int DEFAULT '0',
  `attOr_course` int DEFAULT '0',
  `attOr_det` int DEFAULT '0',
  `attOr_mh` int DEFAULT '0',
  `attOr_sick_lve` int DEFAULT '0',
  `attOr_ex` int DEFAULT '0',
  `attOr_td` int DEFAULT '0',
  `attOr_att` int DEFAULT '0',
  `attOr_awl_osl_jc` int DEFAULT '0',
  `attOr_trout_det` int DEFAULT '0',
  `attOr_present_det` int DEFAULT '0',
  `attOr_present_unit` int DEFAULT '0',
  `attOr_dues_in` int DEFAULT '0',
  `attOr_dues_out` int DEFAULT '0',
  `secondTotal_auth` int DEFAULT '0',
  `secondTotal_hs` int DEFAULT '0',
  `secondTotal_posted_str` int DEFAULT '0',
  `secondTotal_lve` int DEFAULT '0',
  `secondTotal_course` int DEFAULT '0',
  `secondTotal_det` int DEFAULT '0',
  `secondTotal_mh` int DEFAULT '0',
  `secondTotal_sick_lve` int DEFAULT '0',
  `secondTotal_ex` int DEFAULT '0',
  `secondTotal_td` int DEFAULT '0',
  `secondTotal_att` int DEFAULT '0',
  `secondTotal_awl_osl_jc` int DEFAULT '0',
  `secondTotal_trout_det` int DEFAULT '0',
  `secondTotal_present_det` int DEFAULT '0',
  `secondTotal_present_unit` int DEFAULT '0',
  `secondTotal_dues_in` int DEFAULT '0',
  `secondTotal_dues_out` int DEFAULT '0',
  `grandTotal_auth` int DEFAULT '0',
  `grandTotal_hs` int DEFAULT '0',
  `grandTotal_posted_str` int DEFAULT '0',
  `grandTotal_lve` int DEFAULT '0',
  `grandTotal_course` int DEFAULT '0',
  `grandTotal_det` int DEFAULT '0',
  `grandTotal_mh` int DEFAULT '0',
  `grandTotal_sick_lve` int DEFAULT '0',
  `grandTotal_ex` int DEFAULT '0',
  `grandTotal_td` int DEFAULT '0',
  `grandTotal_att` int DEFAULT '0',
  `grandTotal_awl_osl_jc` int DEFAULT '0',
  `grandTotal_trout_det` int DEFAULT '0',
  `grandTotal_present_det` int DEFAULT '0',
  `grandTotal_present_unit` int DEFAULT '0',
  `grandTotal_dues_in` int DEFAULT '0',
  `grandTotal_dues_out` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_company_date` (`company`,`report_date`),
  KEY `idx_company` (`company`),
  KEY `idx_date` (`report_date`),
  KEY `idx_company_date` (`company`,`report_date`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parade_state_daily`
--

LOCK TABLES `parade_state_daily` WRITE;
/*!40000 ALTER TABLE `parade_state_daily` DISABLE KEYS */;
INSERT INTO `parade_state_daily` VALUES (26,'2026-01-24','1 company',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,7,10,2,1,1,0,0,0,0,0,0,4,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,90,81,7,0,16,0,0,0,0,0,0,23,16,58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,115,97,91,9,1,17,0,0,0,0,0,0,27,17,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,115,97,91,9,1,17,0,0,0,0,0,0,27,17,64,0,0,'2026-01-24 00:34:13','2026-01-24 01:57:45'),(31,'2026-01-27','1 company',0,0,3,1,1,0,0,0,0,0,0,0,2,0,1,0,0,0,0,6,1,0,1,0,0,0,1,0,0,3,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,86,8,5,16,0,0,0,1,0,0,30,16,56,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,95,10,6,17,0,0,0,2,0,0,35,17,60,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,95,10,6,17,0,0,0,2,0,0,35,17,60,0,0,'2026-01-27 04:08:02','2026-01-27 04:08:02'),(33,'2026-02-03','2 company',14,2,12,3,1,1,0,0,0,0,0,0,5,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,2,12,3,1,1,0,0,0,0,0,0,5,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,2,12,3,1,1,0,0,0,0,0,0,5,1,7,0,0,'2026-02-03 07:35:48','2026-02-03 07:35:48'),(34,'2026-02-03','HQ company',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,202,16,6,3,2,0,0,4,3,0,34,3,168,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,202,16,6,3,2,0,0,4,3,0,34,3,168,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,202,16,6,3,2,0,0,4,3,0,34,3,168,0,0,'2026-02-03 11:47:39','2026-02-03 11:47:39'),(35,'2026-02-05','1 company',0,0,2,1,0,1,0,0,0,0,0,0,2,1,0,0,0,0,0,5,1,0,0,0,0,0,0,0,0,1,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,98,10,0,16,0,0,0,0,0,0,26,16,72,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,105,12,0,17,0,0,0,0,0,0,29,17,76,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,105,12,0,17,0,0,0,0,0,0,29,17,76,0,0,'2026-02-05 03:05:46','2026-02-05 03:16:21'),(36,'2026-02-05','2 company',0,0,2,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,3,0,0,1,0,0,0,0,0,0,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,70,10,0,0,0,0,0,0,0,0,10,0,60,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,85,11,0,1,0,0,0,0,0,0,12,1,73,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,85,11,0,1,0,0,0,0,0,0,12,1,73,0,0,'2026-02-05 03:10:15','2026-02-05 03:11:01'),(40,'2026-02-11','1 company',5,4,3,1,0,1,0,0,0,0,0,0,2,1,1,0,0,10,8,6,2,0,1,0,0,0,1,0,0,4,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,90,78,16,4,16,0,0,0,3,0,0,39,16,39,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,115,102,87,19,4,18,0,0,0,4,0,0,45,18,42,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,115,102,87,19,4,18,0,0,0,4,0,0,45,18,42,0,0,'2026-02-11 11:16:38','2026-02-11 11:16:38'),(41,'2026-02-11','2 company',10,9,5,1,1,1,0,0,0,0,0,0,3,1,2,0,0,14,12,8,1,1,1,0,0,0,0,0,0,3,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,80,75,70,12,1,6,1,0,0,2,0,0,22,6,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,104,96,83,14,3,8,1,0,0,2,0,0,28,8,55,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,104,96,83,14,3,8,1,0,0,2,0,0,28,8,55,0,0,'2026-02-11 11:19:16','2026-02-11 11:19:16'),(42,'2026-02-11','3 company',7,5,3,1,0,1,0,0,0,0,0,0,2,1,1,0,0,6,6,3,1,0,0,0,0,0,0,0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,60,50,45,11,0,1,0,0,0,0,0,0,12,1,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,73,61,51,13,0,2,0,0,0,0,0,0,15,2,36,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,73,61,51,13,0,2,0,0,0,0,0,0,15,2,36,0,0,'2026-02-11 11:21:06','2026-02-11 11:21:06'),(43,'2026-02-11','HQ company',10,9,6,1,0,1,0,0,0,0,0,0,2,1,4,0,0,30,25,15,4,1,2,0,0,0,0,0,0,7,2,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,190,170,160,25,2,2,1,1,2,2,2,0,37,2,123,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,230,204,181,30,3,5,1,1,2,2,2,0,46,5,135,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,230,204,181,30,3,5,1,1,2,2,2,0,46,5,135,0,0,'2026-02-11 11:23:03','2026-02-11 11:23:03');
/*!40000 ALTER TABLE `parade_state_daily` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personnel`
--

DROP TABLE IF EXISTS `personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `army_number` varchar(100) DEFAULT NULL,
  `rank` varchar(100) DEFAULT NULL,
  `trade` varchar(100) DEFAULT NULL,
  `date_of_enrollment` date NOT NULL,
  `date_of_birth` date NOT NULL,
  `date_of_tos` date DEFAULT NULL,
  `date_of_tors` date DEFAULT NULL,
  `blood_group` varchar(10) DEFAULT NULL,
  `religion` varchar(100) DEFAULT NULL,
  `food_preference` varchar(50) DEFAULT NULL,
  `drinker` varchar(10) DEFAULT NULL,
  `civ_qualifications` text,
  `decoration_awards` text,
  `lacking_qualifications` text,
  `willing_promotions` varchar(10) DEFAULT NULL,
  `i_card_no` varchar(100) DEFAULT NULL,
  `i_card_date` date DEFAULT NULL,
  `i_card_issued_by` varchar(255) DEFAULT NULL,
  `bpet_grading` varchar(50) DEFAULT NULL,
  `ppt_grading` varchar(50) DEFAULT NULL,
  `bpet_date` date DEFAULT NULL,
  `clothing_card` varchar(10) DEFAULT NULL,
  `pan_card_no` varchar(50) DEFAULT NULL,
  `pan_part_ii` varchar(100) DEFAULT NULL,
  `aadhar_card_no` varchar(20) DEFAULT NULL,
  `aadhar_part_ii` varchar(100) DEFAULT NULL,
  `joint_account_no` varchar(100) DEFAULT NULL,
  `joint_account_bank` varchar(255) DEFAULT NULL,
  `joint_account_ifsc` varchar(20) DEFAULT NULL,
  `home_house_no` varchar(255) DEFAULT NULL,
  `home_village` varchar(255) DEFAULT NULL,
  `home_phone` varchar(50) DEFAULT NULL,
  `home_to` varchar(255) DEFAULT NULL,
  `home_po` varchar(255) DEFAULT NULL,
  `home_ps` varchar(255) DEFAULT NULL,
  `home_teh` varchar(255) DEFAULT NULL,
  `home_nrs` varchar(255) DEFAULT NULL,
  `home_nmh` varchar(255) DEFAULT NULL,
  `home_district` varchar(255) DEFAULT NULL,
  `home_state` varchar(255) DEFAULT NULL,
  `border_area` varchar(50) DEFAULT NULL,
  `distance_from_ib` decimal(10,2) DEFAULT NULL,
  `height` decimal(10,2) DEFAULT NULL,
  `weight` decimal(10,2) DEFAULT NULL,
  `chest` decimal(10,2) DEFAULT NULL,
  `identification_marks` varchar(255) DEFAULT NULL,
  `court_cases` text,
  `loan` varchar(50) DEFAULT NULL,
  `total_leaves_encashed` int DEFAULT NULL,
  `participation_activities` text,
  `present_family_location` text,
  `prior_station` varchar(50) DEFAULT NULL,
  `prior_station_date` date DEFAULT NULL,
  `worked_it` varchar(50) DEFAULT NULL,
  `worked_unit_tenure` varchar(255) DEFAULT NULL,
  `med_cat` varchar(50) DEFAULT NULL,
  `last_recat_bd_date` date DEFAULT NULL,
  `last_recat_bd_at` varchar(255) DEFAULT NULL,
  `next_recat_due` date DEFAULT NULL,
  `medical_problem` text,
  `restrictions` text,
  `computer_knowledge` varchar(50) DEFAULT NULL,
  `it_literature` varchar(50) DEFAULT NULL,
  `kin_name` varchar(255) DEFAULT NULL,
  `kin_relation` varchar(100) DEFAULT NULL,
  `kin_marriage_date` date DEFAULT NULL,
  `kin_account_no` varchar(100) DEFAULT NULL,
  `kin_bank` varchar(255) DEFAULT NULL,
  `kin_ifsc` varchar(20) DEFAULT NULL,
  `kin_part_ii` varchar(100) DEFAULT NULL,
  `vehicle_reg_no` varchar(100) DEFAULT NULL,
  `vehicle_model` varchar(255) DEFAULT NULL,
  `vehicle_purchase_date` date DEFAULT NULL,
  `vehicle_agif` varchar(50) DEFAULT NULL,
  `driving_license_no` varchar(100) DEFAULT NULL,
  `license_issue_date` date DEFAULT NULL,
  `license_expiry_date` date DEFAULT NULL,
  `disability_child` varchar(50) DEFAULT NULL,
  `marital_discord` varchar(50) DEFAULT NULL,
  `counselling` text,
  `folder_prepared_on` date DEFAULT NULL,
  `folder_checked_by` varchar(255) DEFAULT NULL,
  `bring_family` varchar(50) DEFAULT NULL,
  `domestic_issues` text,
  `other_requests` text,
  `family_medical_issues` text,
  `quality_points` text,
  `strengths` text,
  `weaknesses` text,
  `detailed_course` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `company` varchar(100) DEFAULT NULL,
  `onleave_status` tinyint(1) DEFAULT '0',
  `detachment_status` tinyint(1) DEFAULT '0',
  `posting_status` tinyint(1) DEFAULT '0',
  `personnel_status` varchar(110) DEFAULT NULL,
  `personnel_remarks` varchar(100) DEFAULT NULL,
  `td_status` tinyint(1) DEFAULT '0',
  `interview_status` tinyint(1) DEFAULT '0',
  `batch` varchar(50) DEFAULT NULL,
  `section` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `army_number` (`army_number`),
  KEY `idx_personnel_army_number` (`army_number`),
  KEY `idx_personnel_name` (`name`),
  KEY `idx_personnel_rank` (`rank`),
  KEY `idx_personnel_rank_category` (`rank`),
  KEY `idx_detachment_status` (`detachment_status`),
  KEY `idx_personnel_company_rank` (`company`,`rank`),
  KEY `idx_personnel_interview_status` (`interview_status`),
  KEY `idx_personnel_army_company` (`army_number`,`company`),
  KEY `idx_personnel_company` (`company`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personnel`
--

LOCK TABLES `personnel` WRITE;
/*!40000 ALTER TABLE `personnel` DISABLE KEYS */;
INSERT INTO `personnel` VALUES (1,'MOHAN LAL','JC457693','Subedar Major','jene','1999-09-12','1980-12-12','2025-12-09','2012-12-30','B+','HINDu','Vegetarian','No','12th',NULL,NULL,'Yes','F-712930','1999-03-09','COMDT 3MTR',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'RAJASTHAN',NULL,NULL,190.00,89.00,90.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-02 15:20:00','2026-02-03 03:17:50',NULL,0,0,0,NULL,NULL,0,0,NULL,NULL),(38,'Hansram ','jc393919L','Naib Subedar','jene','2012-02-09','1993-02-02','2024-11-11','2024-12-12','O+','hindu','Vegetarian','No',NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'RAJASTHAN',NULL,NULL,176.00,72.00,90.00,'bl mole',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-23 20:28:40','2026-02-12 05:41:57','2 Company',0,0,0,NULL,NULL,0,0,NULL,'IT'),(39,'JITENDRA SINGH','15730189W','NK','TTC','2011-09-27','1993-02-20','2022-12-31','2023-02-07','B+','HINDU','Vegetarian','No','B.A.',NULL,NULL,'Yes','F-512860','2012-02-22','COMDT 3MTR','EX','GOOD','2024-12-18','Yes','EWFPS9668F','0/0400/0004/2022','327717991162','0/0734/0004/2018','20109409422','SBI','SBIN0002433',NULL,'RAIPUR','9368899393','RAIPUR','RAIPUR','NAUJHEEL','MANT','MATHURA','MATHURA','MATHURA','UTTAR PRADESH','No',NULL,178.00,76.00,90.00,'BM 4CM LT NIPPLE 1 O CLOCK',NULL,'Yes',177,NULL,'DIST-MATHURA STATE - UP',NULL,NULL,'Yes','NFS, 33 MONTH','No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','MRS PRIYA','WIFE','2018-12-07','20109409422','SBI','SBIN0002433','0/0400/0003/2022',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,'No','2026-01-23 20:38:07','2026-01-28 10:24:26','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(40,'SENTHIL KUMAR G','15720341L','NK','TTC','2010-04-09','1989-02-13','2023-01-01','2023-02-15','B+','HINDU','Non-Vegetarian','No','BCA',NULL,NULL,'Yes','F-065987','2010-08-25','COMDT 3 MTR','GOOD','GOOD',NULL,'Yes','BYHPK1522M','0/0165/0006/2013','331591522038','0/0451/0006/2015','20069915790','SBI','SBIN0003373','3-1-4A','CHINNALAPATHI','8838508774','AUTHUR','CHINNALAPATHI','CHINNALAPATI','AUTHOOR','DINDUGU','CHENNAI','DINDIGUL','TAMILNADU',NULL,NULL,180.00,85.00,NULL,'BM FRONT OFLEFT JT',NULL,'Yes',NULL,NULL,NULL,NULL,NULL,'Yes',NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','RAJALAKSHMI','WIFE','2018-02-18','20069615190','SBI','SBIN0003313',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-23 22:58:56','2026-01-24 23:04:04','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(41,'GIRI AJINATH BABAN','15743230A','L NK','TTC','2025-06-28','1996-05-23','2023-04-17','2023-07-11','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','f-772534','2016-01-22','COMDT 3 MTR','GOOD','GOOD',NULL,'Yes','BQBPG9296C','3/3324/0022/2016','805658111145','3/1997/0010/2016','35110590222','SBI','SBIN0005995',NULL,'GHATSHILPARGAON','8379001887','SHIRAR ','GHATSHIL PARGAON','SHIRAR','SHIRAR','AHMEDNAGAR ','AHMADNAGAR','BEED','MAHARASHTRA','No',NULL,168.00,67.00,85.00,'BM UPPER 113 RT ARM',NULL,'Yes',100,NULL,NULL,NULL,NULL,'Yes','28 MONTHS','No',NULL,NULL,NULL,NULL,NULL,'Excellent',NULL,'GIRI NEHA','WIFE','2020-08-13','30110590222','SBI','SBIN0005998','0/00098/0004/2022',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-23 23:20:34','2026-02-07 03:46:16','1 Company',0,0,0,NULL,NULL,0,0,NULL,NULL),(42,'MOHAN KUMAR YADAV','15736949K','NK','TTC','2013-09-17','1992-05-05','2023-01-13','2023-02-26','B+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','F-704506','2014-03-10','COMDT 1STC','EX','EX','2025-10-09','Yes','AKTPY5260B','3/1600/0005/2014','620720821638','3/1576/0028/2015','33364425812','SBI','SBIN0008132','115','SINGHPUR ','8298347320','BALAHAPUR ','NAYAGWON','NAYAGWON','BEGUSARIA','BEGUSARIA','DANAPUR','BEGUSARIA','RBIHAR','No',NULL,172.00,77.00,85.00,'BM 5CM LT NIPPLE 12O CLOCK',NULL,'Yes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','KANCHAN KUMARI','WIFE','2016-04-22','33364425812','SBI','SBIN0008132','0/0321/0030/2025',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-23 23:40:20','2026-02-03 03:17:50','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(45,'DHANANJAY KUMAR YADAV','15740970K','NK','TTC','2014-09-26','1993-07-01','2024-01-02','2024-01-11','AB+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','F-706427','2015-04-25','CMDT 1 STC','EX','EX',NULL,'Yes','AMHPY9168N',NULL,NULL,NULL,'202485572422','SBI','SBIN0011244',NULL,'SONARI',NULL,NULL,'GOTHAIN','NAGRA','RASRA','BALLIA','VANARASI','BALLIA','UTTAR PRADESH',NULL,NULL,169.00,74.00,NULL,'A BLACK MOLE ON RT SHOULDER',NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'PRIYANKA YADAV','WIFE','2018-03-11','20248572422','SBI','SBIN0011244','0/000/005/2020',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 00:12:17','2026-02-03 04:19:15','1 Company',0,1,0,NULL,NULL,0,0,NULL,'MW'),(50,'SUNIL GODARA','A4203413X','Agniveer','TTC','2023-10-23','2004-10-21','2024-06-04','2024-06-19','B+','HINDU','Vegetarian','No','BA',NULL,NULL,'Yes','G-346223','2023-12-19','COMDT 1STC','EX','EX','2025-10-11','Yes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'RD 78','SARDARPURA KHUROL','7568770188','NUWA','NUWA','MAULAHAS','DIDWARA','KUCHAMAN','DIDWARA','NAGAUR','RAJASTHAN','No',NULL,179.00,62.50,82.00,'A BLACK MOLE ON RIGHT HAND ANGLE',NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','RAMSWAROOP','FATHER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 01:10:11','2026-02-03 08:32:08','1 Company',0,1,0,NULL,NULL,0,0,'Batch 3','MW'),(51,'ANKIT SINGH TOMAR','A4204811L','Agniveer','TTC','2023-10-31','2003-06-03','2024-06-05','2024-06-21','B+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','G346828',NULL,'COMDT 1 STC','EX','EX','2025-09-14','Yes','COKPP6647G',NULL,'552653347322',NULL,'20511518025','SBI','SBIN0010846',NULL,'KHUSHAL KAPURA','9103272494','RANHERA','RANHERA','MAHUA','PARSA','GAWALIOR','GAWALIOR','MURENA','MADHYA PRADESH','No',NULL,173.00,67.00,85.00,NULL,NULL,'Yes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','ANJU DEVI','MOTHER',NULL,'20511518025','SBI','SBIN0010846',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','2026-01-24 01:26:11','2026-01-28 11:45:39','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','MW'),(52,'UDAY KUMAR','A4203816X','Agniveer','TTC','2023-10-25','2003-12-09','2024-06-04','2024-07-03','B+','HINDU','Non-Vegetarian','No','BSC,COMPUTER COURSE, ITI',NULL,NULL,'Yes','G-387912','2023-12-02','COMDT 1STC','EX','EX','2025-10-13','Yes','LWFPK7672G',NULL,'881525033809',NULL,'42350031902','SBI','SBIN0001240',NULL,'CHANDIPUR','9931791006',NULL,'MAKANPUR','WARISALIGANJ','WARISALIGANJ','WARISALIGANJ','GAYA','NAWADA','BIHAR',NULL,NULL,170.00,68.00,85.00,'A MOLE MARK ON THE CHEST',NULL,'No',NULL,'FOOTBALL','CHANDIPUR','No',NULL,'No',NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 18:13:13','2026-02-10 11:54:31','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','MW'),(56,'RAJPUT VIKAS','A4351981P','Agniveer','TTC','2023-02-25','2002-06-25','2025-08-25','2025-09-02','B+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','G-076497','2023-04-20','COMDT 3 MTR','EX','EX','2025-06-15','Yes','EXAPR5445D',NULL,'373864729378',NULL,NULL,NULL,NULL,'549','AHMEDABAD','7698721433',NULL,'KUBER NAGAR','MEGHARNAGAR','AHMEDABAD','AHMEDABAD','AHMEDABAD','AHMEDBAD','GUJRAT',NULL,NULL,168.00,59.00,80.00,'A SMALL MOLE ONRIGHT HAND LAST FINGURE',NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','VINOD SINGH','FATHER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 19:05:17','2026-01-28 07:04:52','1 Company',0,0,0,NULL,NULL,0,0,'Batch 2','MW'),(57,'BRAJESH TIWARI','15740527W','NK','TTC','2014-07-02','1991-05-08','2025-10-01','2025-11-09','O+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','F-706175','2015-02-21','COMDT 1STC','EX','EX','2025-09-05','Yes','AVQPT7233H','3/2204/2014/2810/2014','830640143784','3/1965/0010/2805/2015','629003800041614','PNB','PUNB0233600',NULL,'KATRA GHANSHYAM','8423914620','SACHINDI','SACHINDI','SACHINDI','SADAR','KANPUR CENTRAL','KANPUR NAGAR','KANPUR NAGAR','UTTAR PRADESH','No',NULL,172.00,69.00,85.00,NULL,NULL,'Yes',162,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','ANUBHA TRIPATHI','WIFE','2020-02-25','629003800041614','PNB','PUNB0233600',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 19:44:00','2026-02-03 09:23:30','1 Company',1,0,0,NULL,NULL,0,0,NULL,'MW'),(58,'SWAPANIR KUMAR','157606852K','Signal Man','TTC','2006-12-12','1986-07-05','2025-10-24','2025-11-07','AB+','HINDU','Vegetarian','No','GRADUATE',NULL,NULL,'Yes','F-712937','2015-06-27','COMDT 3 MTR','EX','EX',NULL,'No','BMBPK1603D','0/0046/0016/2012','422526578375','0/0422/0019/2015','50100774011260','HDFC',NULL,NULL,'PIMMA MIWADA','79017322919','KANPUR','KARWAN','RASULABAD','RASULABAD','BILHAUR','KANPUR','KANURDEHAT ','UTTAR PRADESH','No',NULL,173.00,71.00,80.00,'A BM ON NOSE',NULL,'Yes',151,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'KALPANA DEVI','WIFE','2012-02-15','50100774011260','HDFC',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 23:33:09','2026-02-11 11:31:50','1 Company',0,0,0,NULL,NULL,1,0,NULL,'MW'),(60,'BRIJESH KUMAR TIWARI','15731634W','NK','LMN','2012-07-24','1994-06-20','2025-10-07','2025-11-13','O+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','F-502263','2013-01-07','COMDT 1 STC','GOOD','GOOD','2025-09-25','Yes','ARYPT1962F','3/1810/0012/2013','230568651800','0/0182/0026/2015','32475715182','SBI','SBIN0012180',NULL,'BADHARA ','7898991662','SEMARIYA','BADHARA ','SEMARIYA','SEMARIYA','REWA','JABALPUR','REWA','MADHYA PRADESH','No',NULL,171.00,66.00,85.00,'BM 2CM INFRONT RT EAR',NULL,'Yes',128,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','NEELAM TIWARI','WIFE','2017-02-28','32475715182','SBI','SBIN0012180','0/0568/0001/2025',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-24 23:51:48','2026-01-28 11:50:20','1 Company',0,0,0,NULL,NULL,0,0,NULL,'LINE'),(61,'ARVIND GUPTA','15740824K','NK','TTC','2014-09-21','1994-05-10','2025-10-02','2025-10-24','B-','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-712278','2015-02-17','COMDT 3 MTR','SAT','GOOD',NULL,'Yes','BOMPG3668F','0/0280/0006/2017','340532482464','3/1936/0007/2015','34287934452','SBI','SBIN0016748',NULL,'RAJAULA','9305437081',NULL,'ISPHATIC SHILL','NAYA GAON','MAJHGAWAN','CHITRAKOOT','PRAYAGRAJ','SATNA','MADHYA PRADESH','No',NULL,170.00,73.00,85.00,'A BM ON RT SHOULDER',NULL,'Yes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','PRIYANKA GUPTA','WIFE','2017-06-02','34287934452','SBI','SBIN0016748','0/0571/0004/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 00:03:16','2026-01-28 11:48:26','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(64,'ADARSH S','15719460P','HAV','OCC','2010-03-18','1992-05-31','2023-11-18','2023-12-18','A+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','F-065571','2010-08-12','COMDT 3 MTR',NULL,NULL,NULL,'Yes','BEIPA7284M','0/0033/0003/2013','504162583308','0/0189/0037/2015','20061299339','SBI','SBIN0010691','9/397/B','KALATHUMMAL','9567212167','KATTAKADA','KARUTHAMCODE','KATTAKADA','KATTAKADA','TRIVANDRUM','TRIVANDRUM','TRIVANDRUM','KERALA',NULL,NULL,174.00,84.00,NULL,NULL,NULL,'Yes',163,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','ARYADEVI S ','WIFE','2017-10-27','20061299339','SBI','SBIN0010691','0/0016/0001/2018',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 00:23:47','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'OP'),(66,'SR PANDEY','15689681K','HAV','OCC','2003-12-01','1984-08-15','2023-03-22','2023-04-28','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','E-521960','2004-05-01','COMDT 1STC','EX','EX',NULL,'Yes','APRPP6884P','0/0165/0021/2014','678648364850','0/0056/0023/2015','30401445307','SBI','SBIN0015348','43','SARSWAN','9511058026','ARJUNGANJ','ARJUNGANJ','LUCKNOW CANT','SAROJININAGAR','LUCKNOW','CH CC LUCKNOW','LUCKNOW','UTTAR PRADESH','No',NULL,183.00,82.00,NULL,'BM OVER RT SHOULDER',NULL,NULL,291,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'NEELAM PANDEY','WIFE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 00:48:51','2026-02-11 11:32:44','1 Company',0,0,1,NULL,NULL,0,0,NULL,'OP'),(67,'S K GUPTA','15716045H','NK','OCC','2009-06-26','1986-08-10','2024-05-21','2024-06-27','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-165455','2009-12-09','COMDT 1STC',NULL,NULL,NULL,'Yes','BBBPG2830D','0/0018/0003/2017','495371840419','0/0045/0011/2016','41803387570','SBI','SBIN0007191','221','GOHARI','7518576522','PHAPHAMAU','GOHARI','PHAPHAMAU','SORUON','PRAYAGRAJ','PRAYAGRAJ','PRAYAGRAJ','UTTAR PRADESH',NULL,NULL,170.00,73.00,85.00,'BM LEFT PALM',NULL,'No',156,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','SONI SAHOO','WIFE','2022-02-18','41803387570','SBI','SBIN0007191','0/0172/0005/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 01:30:04','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'OP'),(68,'RASHID','15728668I','NK','OCC','2011-06-28','1990-02-19','2023-09-21','2023-10-22','O+','MUSLIM','Vegetarian','No','12th',NULL,NULL,'Yes','F-342886','2011-12-03','COMDT 3MTR',NULL,NULL,NULL,'Yes','BILPR3901E',NULL,NULL,NULL,'20106858347','SBI','SBIN0008000','46','IMDRWAM','8738984125','KATILA','KATILA','JANGIPUR','GHAZIPUR','VARANASI','VARANASI','GHAZIPUR','UTTAR PRADESH','No',NULL,176.00,76.00,80.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 01:54:50','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'OP'),(71,'MANE PRAIWAL K','A4354369W','Agniveer','OCC','2024-04-24','2003-09-17','2024-12-05','2025-12-08','B+','HINDU','Non-Vegetarian','No','10th, ITI',NULL,NULL,'Yes','G-329375','2024-06-18','COMDT 3 MTR','EX','EX','2025-07-27','Yes','HNJPM5298D',NULL,'350984333070',NULL,'20521110218','SBI','SBIN0011136','347','HAROLI','9766732682',NULL,'HAROLI','SHIROL','SHIROL','MIRAJ','KOLHAPUR','KOLHAPUR','MAHARASHTRA','No',NULL,169.00,62.00,72.00,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','MANE PRAJWAL','MOTHER',NULL,'20521110218','SBI','SBIN0011136',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 02:24:30','2026-01-28 12:18:09','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','OP'),(72,'BATTINI RANGASWAMY','15734096Y','NK','OCC','2013-03-14','1993-06-15','2023-12-20','2024-01-05','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-503487','2013-07-31','COMDT 1STC',NULL,NULL,NULL,NULL,'EWUPS8535Q','0/0129/0002/2018','410525507722','0/0128/0018/2018','32908641551','SBI','SBIN0008305','2-21','CHOLLAVEEDU',NULL,'GIDDALUR','CHOLLAVEEDU','RACHERLA','RACHERLA','GIDDALUR','SECUNDRABAD','PRAKASAM','ANDHRA PRADESH',NULL,NULL,169.00,68.00,85.00,NULL,NULL,'No',142,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'B ANUSHA ','WIFE','2019-04-22','32908691551','SBI','SBIN0008305','0/0224/0005/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 02:40:22','2026-02-04 14:48:39','1 Company',0,0,0,NULL,NULL,0,0,NULL,'OP'),(76,'PATIL AKASJ RAJARAM','A4354515L','Agniveer','OCC','2024-04-24','2002-12-23','2024-12-05','2025-01-09','A+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-328892','2024-06-11','COMDT 3 MTR','EX','EX',NULL,'Yes','ICJPP6639D',NULL,'377141514726',NULL,'20521111030','SBI','SBIN0011644','89','SHEDGEWADI','8082519425','SHEDGEWADI','NATHAWADE','KAKRUD','PUNE','KARAD','PUNE','SANGLI','MAHARASHTRA','No',NULL,176.00,60.00,83.00,'A BMON RT CHEEK',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:06:28','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','OP'),(77,'SHAHIL','A4353823Y','Agniveer','occ','2024-04-24','2003-08-01','2024-12-04','2025-01-04','A+','HINDU','Vegetarian','No','12TH',NULL,NULL,'Yes','G-329731','2024-06-25','COMDT 3 MTR','EX','EX',NULL,'Yes','PFDPS4959M',NULL,'239743162265',NULL,'20520656289','SBI',NULL,NULL,'GHANA','8875989574','GHANA','GHANA','NECHHWA','NECHHWA','SIKAR','JAIPUR','SIKAR','RAJASTHAN','No',NULL,176.00,70.00,83.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','SUNITA DEVI','MOTHER',NULL,'20520656289','SBI','SBIN0032348',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:12:26','2026-02-03 08:32:08','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','OP'),(78,'PRADEEP BABU','15717264F','NK','TTC','2009-09-26','1990-01-11','2024-02-21','2024-04-21','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-165958','2010-02-06','COMDT 1STC',NULL,NULL,NULL,'Yes','PDYBP1630B','0/129/0010/2017','900201878694','0/118/0038/2015','30999786128','SBI','SBIN0010317',NULL,'SASIA HUSAIPUR',NULL,'C B GANJ','SADAR','CB GANJ','BAREILLY','BAREILLY','BAREILLY','BAREILLY','UTTAR PRADESH',NULL,NULL,170.00,70.00,85.00,'BM ON RIGHT SHOULDER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:20:21','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'OP'),(79,'ADARASH KUMAR SABU','A4200038M','Agniveer','OCC','2022-12-25','2004-01-01','2025-04-13','2025-04-29','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-105798','2023-02-28','COMDT 1STC','EX','EX','2025-04-09','Yes','QDPPS1760F',NULL,'715154612450',NULL,'20211499066','SBI','SBIN0003534','06','SUKUMAR','9797559993',NULL,'DPA','KURA','KURA','LOHARADAGU','RANCHI','LOHARDAGA','JHARKHAND',NULL,NULL,170.00,63.00,85.00,'BM 5CM 2 O CLOCK FROM RT NIPPLE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'KALAWATI DEVI','MOTHER',NULL,'20511499066','SBI','SBIN0003534',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:30:35','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','OP'),(80,'LAXMAN MUNDA','15724953A','NK','OCC','2011-03-16','1988-11-17','2024-01-01','2024-02-07','AB+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-169896','2011-08-24','COMDT 1STC',NULL,NULL,NULL,'Yes','BPNPM0997M','0/0070/0019/2013','609915094389','0/0240/0018/2015','31796445273','SBI','SBIN0001081',NULL,'BELASAREI','9797118633','MACHHAGARH','GHOLAKUND','PATNA','SAHARPARA','BHUBANESWAR','KOLKATA','KEONJHAR','ODISHA','No',NULL,170.00,72.00,85.00,'BM RT FOREAREN 9CM BELOW ELBOW',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'INDUMATI KANDEYANG','WIFE','2015-03-03','31796445275','SBI','SBIN0001081','0/0249/0003/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:37:51','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'OP'),(81,'SUNIL KUMAR','15720596L','NK','EFS','2010-06-08','1988-08-16','2023-10-17','2023-11-16','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-167757','2010-11-13','COMDT 1STC','EX','EX',NULL,'Yes',NULL,NULL,'660451015340','0/604/0012/2018',NULL,NULL,NULL,NULL,'BHALUATAR','6204442136','NAWADA',NULL,'MUFASIL','NAWADA','GAYA','GAYA','NAWADA','BIHAR','No',NULL,173.00,75.00,84.00,'RIGHT HAND MOLE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'BEBI DEVI ','WIFE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:47:25','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'PWR'),(82,'RAVI','A4204797K','Agniveer','EFS','2023-10-31','2003-08-07','2024-06-05','2024-06-20','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-387930','2023-12-02','COMDT 1STC',NULL,NULL,NULL,'Yes','GUSPR8950N',NULL,'465418459596',NULL,'20511518900','SBI','SBIN0000430',NULL,'NANDPURA','8485682092','NANDPURA','NANDPURA','DEVGHAR','JOURA','GWALIOUR','GWALIOR','MORENA','MADHY PRADESH',NULL,NULL,174.00,60.00,85.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'SANTOSHI','MOTHER',NULL,'20511518900','SBI','SBIN0000430',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 19:53:47','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','PWR'),(83,'RAM SINGH','15688598A','HAV','EFS','2003-09-23','1981-06-20','2024-07-14','2024-07-24','O+','HINDU','Non-Vegetarian','No','B.A.',NULL,NULL,'Yes','F-521715','2004-02-28','COMDT 1STC','GOOD','EX','2024-05-27','Yes','BJTPS6779R','0/0200/0028/2012','365571169260','0/0046/0036/2015','20034675737','SBI','SBIN0002596',NULL,'ASWALPUR','8808511711','PINDRA','PHOOLPUR','PINDRA','PINDRA','VARANASI','VANARASI','VANARASI','UTTAR PRADESH',NULL,NULL,17.00,NULL,85.00,'2 BM BELOW LEFT EYE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','BABITA DEVI','WIFE','2014-12-07','20034675737','SBI','SBIN0002596','0/0560/0009/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 20:01:56','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'PWR'),(84,'RAJESH CHAURASIA','15716216K','HAV','EFS','2009-06-29','1987-08-14','2024-07-05','2024-07-15','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','E-933944','2009-12-15','COMDT 3 MTR','EX','EX',NULL,NULL,'ARWPC3055A','0/0082/2012','418132647346','0/0532/000/2015','75058454393','SBI',NULL,'376','KHARAUNI','7252984594','KHARAUNI','KHARAUNI','BANSDIH','BANSDIH','BALLIA','VANARASI','BALLIA','UTTAR PRADESH',NULL,NULL,177.00,72.00,80.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'PRIYANKA','WIFE','2015-09-15','75058454393','SBI',NULL,'0/0047/2018',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 20:11:29','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'PWR'),(85,'SUNIL KUMAR YADAV','15709802K','NK','EFS','2008-03-21','1987-03-01','2024-08-28','2024-10-03','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','E-929453','2008-08-16','COMDT 3 MTR','GOOD','GOOD',NULL,NULL,'AHXPY7607F','0/0430/0032/2012','338433386429','0/0133/0012/2015','30606854135','SBI','SBIN0014526',NULL,'GOVINDPUR','9334030074','MAHESHKHUNT','MAHESHKHUNT','MAHESHKHUNT','GOGARI','MAHESHKHUNT','DANAPUR','KHAGARIA','BIHAR',NULL,NULL,172.00,64.00,86.00,'BM 2CM BELOW LEFT ELBOW',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'PINKI DEVI','WIFE','2009-02-15','30606854135','SBI','SBIN0014526','01/0009/0001/2019',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 20:19:19','2026-01-28 07:14:19','1 Company',0,0,0,NULL,NULL,0,0,NULL,'PWR'),(86,'GHANSHYAM MAHLA','15718811M','HAV','TTC','2010-01-05','1991-08-20','2024-01-16','2024-02-12','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-166851','2010-06-28','COMDT 1STC','EX','EX',NULL,'Yes','BKLPM4602A','0/0588/0003/2016','506470183601','0/0188/0008/2015','31106104091','SBI','SBIN0003874',NULL,'MAHLA KI DHANI','9981942440','SIKAR','SIHOT BARI','LOSAL','SIKAR','SIKAR','JAIPUR','SIKAR','RAJASTHAN','No',NULL,182.00,78.00,92.00,'BLACK MOLE RIGHT TEMPLE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'SANJU DEVI','WIFE','2012-12-10','31106104091','SBI','SBIN0003874','0/0337/0007/2024',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 20:29:03','2026-02-03 08:32:08','1 Company',0,0,0,NULL,NULL,0,0,NULL,'NCO IT'),(88,'JINCE L','15731820M','HAV','TTC','2012-09-08','1994-04-29','2022-09-08','2024-10-12','O+','CHRISTIAN','Non-Vegetarian','No','B.A. ENGLISH',NULL,NULL,'Yes','E-065976','2022-10-20','COMDT 3 MTR','GOOD','GOOD','2025-02-05','Yes','ALKPL5481B','3/0209/0001/2014','653071336447','0/0263/0012/2015','20054990754','SBI','SBIN0071137',NULL,'KOLLEMCODE','8300797369','KOLLEMCODE','KOLLEMCODE','KOLLEMCODE','VILAVANCODE','TRIVANDRUM','TRIVANDRUM','KANYA KUMARI','TAMILNADU','No',NULL,177.00,75.00,85.00,'A BM ON THE CHEST',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','DIVYA MOL','WIFE','2021-06-24','20054990754','SBI','SBIN0071137','0/0037/0003/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 20:41:55','2026-02-12 05:41:57','1 Company',0,0,1,NULL,NULL,0,0,NULL,'IT'),(89,'JEBIN PAUL K','15740143F','NK','TTC','2014-06-20','1996-01-14','2023-12-15','2024-01-15','B+','CHRISTIAN','Vegetarian','No','12th',NULL,NULL,'Yes','F-706001','2014-11-22','COMDT 1STC','EX','EX',NULL,'Yes','DPSPK7104B','3/851/0015/2014','511990094796','3/1910/00029/2015','20244730279','SBI','SBIN0071121','KUTTIVILA KIZHALKATHI VEEDU','NEDUMPANA','8943371661','NEDUMPANA','NEDUMPANA','CHATHANNOOS','KOLLAM','KOLLAM JN','TRIVENDRUM','KOLLAM','KERALA',NULL,NULL,182.00,90.00,NULL,'BM ON BELOW LEFT NIPPLE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','DE ATHIRA KRISHNAN','WIFE','2021-12-29','20244730279','SBI','SBIN0071121','0/0125/0007/2022',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 20:58:40','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,NULL,'IT'),(90,'MD SUJAN MIRZA','15749660A','NK','OCC','2016-06-15','1997-10-10','2024-02-06','2024-03-14','A+','ISLAM','Non-Vegetarian','No','12th',NULL,NULL,'Yes','F-820680','2016-12-13','COMDT 3 MTR',NULL,NULL,NULL,'Yes','COOPM7257M','3/0664/0040/2016','268884194930','0/0286/0012/2018','42784506487','SBI','SBIN0013985',NULL,'MUDDA','9564202863','KANDI','KULI KANDI','BWRWAN','KANDI','KGLE','CH  EC','MURSHIDABAD','WEST BENGAL',NULL,NULL,182.00,83.00,89.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','MOUSUMI BEGAM','WIFE','2023-02-20','42784506487','SBI','SBIN0013985','0/0259/0010/2024',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 21:07:00','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,NULL,'IT'),(91,'MOHANRAJ T','15753860N','NK','TTC','2017-06-17','1995-05-28','2023-01-01','2023-02-17','B-','HINDU','Non-Vegetarian','No','B TECH',NULL,NULL,'Yes','G-056102','2017-12-16','COMDT 1STC','EX','EX','2025-10-23','Yes','CWUPM2914B','3/0381/0003/2018','611930102185','3/0359/0023/2018','20447385551','SBI','SBIN0014822','8B','KULAVILAKKU','7373305452',NULL,'KAGAM','SIVAGIRI','MODAKKURICHI','ERODE','CHENNAI','ERODA','TAMILNADU',NULL,NULL,180.00,76.00,NULL,'BM MIDDLE .3 RT COLLAR BONE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','LOGESH T','WIFE','2021-11-15','20447385551','SBI','SBIN0014822','0/0601/005/2022',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-25 21:15:15','2026-02-07 13:52:21','1 Company',0,0,0,NULL,NULL,0,0,NULL,'IT'),(92,'ASWIN M','A4201316F','Agniveer','LMN','2023-02-22','2001-02-13','2025-08-23','2025-09-15','O+','HINDU','Non-Vegetarian','No','B.COM',NULL,NULL,'Yes','G-237946','2023-04-11','COMDT 1STC','EX','GOOD',NULL,'Yes','GPRPM6808G',NULL,'583616131870',NULL,NULL,NULL,NULL,'558/ KOCHUVEEDU VADAKKATHIL','KAREEPRA','7736292967','KOTTARAKARA','NEUIMUKKU','EZHUKONE','KOTTARAKARA','KOLLAM','PANGODU TRIVANDRUM','KOLLAM','KERALA','No',NULL,172.00,65.00,NULL,'A BM ON LEFT CHEST',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No','No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 01:34:49','2026-02-01 06:11:33','1 Company',1,0,0,NULL,NULL,0,0,'Batch 2','IT'),(93,'GAIKWAD RAHUL SUNIL','A4204643X','Agniveer','TTC','2023-10-28','2002-12-05','2025-06-25',NULL,'O+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-346286','2023-12-13','COMDT 1STC','EX','EX',NULL,'Yes','DNKPG5253B',NULL,'829657549687',NULL,'50100676149931','HDFC','HDFC0004181',NULL,'PALDHAG',NULL,'BULDANA','KOTHALI','BULDANA','BULDANA','BHUSAWAL','AHMADNAGAR','BULDANA','MAHARASHTRA','No',NULL,171.00,59.00,NULL,'MOLE ON RIGHT HAND',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 17:08:09','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','IT'),(94,'VIVEK KUMAR SRIVASTAV','A4352497P','Agniveer','TTC','2023-10-23','2003-10-02','2024-06-05','2024-06-20','B+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-235430','2023-12-05','COMDT 3 MTR',NULL,NULL,NULL,'Yes','PBMPS2516A',NULL,'986429176586',NULL,'922010056317271','AXIS','UTIB0000078','T-488 GALI NO-2','BALJEET NAGAR ','7836869031',NULL,'PATEL NAGAR','PATEL NAGAR','KAROL BAGH','NEW DELHI','DELHI CANTT','CENTRAL DELHI','NEW DELHI',NULL,NULL,174.00,63.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','LAXMI SRIVASTAV','MOTHER',NULL,'922010056817271','AXIS','UTIB0000078',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 17:16:25','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','IT'),(95,'ROSHAN KESHARWANI','A4203079F','Agniveer','TTC','2023-02-25','2001-07-17','2025-08-25','2025-09-07','AB+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-237867','2023-04-10','COMDT 1STC','GOOD','GOOD','2025-08-21','Yes','KCUPK1282C','4/00110/2025/171802714','221854693956','4/0036/2025/801414',NULL,NULL,NULL,NULL,'BHILAI','8357050793','SECTOR-I','SECTOR-I','CHAWANI','DURG','DURG','JABALPUR','DURG','CHHATTISGARH','No',NULL,170.00,65.00,83.00,'BM OVER RT SHOULDER FRONT SIDE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','MAMTA KESHARWANI','MOTHER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 17:26:58','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,'Batch 2','IT'),(96,'GIDIJALA VENNKATA RAMANA ','A4351064L','Agniveer','OCC','2022-12-26','2002-08-25','2025-04-05','2025-04-21','O+','HINDU','Non-Vegetarian','No','12th, ITI',NULL,NULL,'Yes','G-074505','2023-02-27','COMDT 3 MTR','EX','EX',NULL,'Yes',NULL,NULL,'608158759407',NULL,NULL,NULL,NULL,'1-114','V R R PURAM','8082158339',NULL,'PEDDA SRILAM','R AMADALAVALASA','R AMADALAVALASA','VIZIANGARAM','VISHAKPATNAM','VIZIANGARAM','ANDHRA PRADESH','No',NULL,171.00,59.00,85.00,'BM 2.5 CM ABOVE OUTER END OF  THE EYE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','RAMANAMMA','MOTHER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 17:37:51','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','IT'),(97,'EROTHU RAKESH','A4351041K','Agniveer','OCC','2022-12-26','2000-06-13',NULL,NULL,'B+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-074482','2023-02-27','COMDT 3 MTR',NULL,NULL,NULL,'Yes','ADVPE6644G',NULL,'476275416267',NULL,NULL,NULL,NULL,'5-2-68','BARUVA','7660870085',NULL,'BARUVA','BARUVA','SOMPETA','PALASA','VISHAKHAPATNAM','SRIKAKULAM','ANDHRA PRADESH','No',NULL,169.00,61.00,85.00,'BM RT UPPER .3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 17:42:45','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','IT'),(98,'SHAILENDRA SINGH','1574165Y','NK','TTC','2015-03-20','1994-03-24','2025-10-16','2025-11-02','B+','HINDU','Non-Vegetarian','Yes','GRADUATE',NULL,NULL,'Yes','F-713305','2025-08-26','COMDT 3 MTR','GOOD','GOOD','2025-07-04','Yes','GBNPS3324F','3/2970/0022/2015','698459171387','3/2969/0013/2015','34866861178','SBI','SBIN0030182','32','BARKHEDA JAI SINGH','9797623284','BALAGUDA','BALAGUDA','PIPLIA MANDI','MALHARGARH','PIPLIA MANDI','KOTA MHOW',NULL,'MADHYA PRADESH','No',NULL,178.00,74.00,90.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Yes','2025-09-26','PUNE','2026-03-12','ACUTE BRONCHITIS','AS PER MED BD','Excellent','Excellent','RANU KUNWAR DEWADA','WIFE','2018-03-05','34866861178','SBI','SBIN0030182','0/0517/0001/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 18:01:21','2026-02-12 05:41:57','1 Company',0,0,0,NULL,NULL,0,0,NULL,'IT'),(99,'PANDURANG B K','15692903Y','HAV','TTC','2004-03-24','1983-05-16','2023-01-14','2023-03-02','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','E-719670','2004-08-21','COMDT 3 MTR','EX','EX',NULL,'Yes','AROPK0205E','0/0138/0022/2012','664729835490','0/0216/0003/2015','20033775845','SBI','SBIN0000415',NULL,'ZOLICHA KOND','8830886518','M.I.D.C. MAHAD','WALAN','M.I.D.C. MAHAD','MAHAD','VEER','MUMBAI','RAIGAD','MAHARASHTRA','No',NULL,170.00,70.00,NULL,'BM ON RT WRIST JOINT',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','SARITA','WIFE','2008-08-13','20033775845','SBI','SBIN0000415','0/0049/0003/2020',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 18:12:53','2026-01-28 07:04:52','1 Company',0,0,0,NULL,NULL,0,0,NULL,'CHQ'),(100,'AMIT RANJAN','15720931K','HAV','OP CIPH','2010-06-24','1988-02-21','2022-12-31','2020-01-17','B+','HINDU','Vegetarian','Yes','12th',NULL,NULL,'Yes','F-066605','2010-11-13','COMDT 3 MTR','EX','EX',NULL,'Yes','AZVPR4171J','0642/356/2012',NULL,NULL,'20069618859','SBI','SBIN0014293',NULL,'BISHANPUR','6006683105','BISHANPUR','PAHARPUR','BIELUPUR',NULL,'PATNA','DANAPUR','VAISHALI','BIHAR','No',NULL,174.00,74.00,84.00,'BM RT ARM',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','NIDHI KUMARI','WIFE','2012-04-14','20069618859','SBI','SBIN0014293','63306/002/2024',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 18:21:09','2026-01-28 07:04:52','1 Company',0,0,0,NULL,NULL,0,0,NULL,'CHQ'),(101,'T. RAMESH BABU','15681641N','HAV','LMN','2003-01-27','1982-06-16','2023-01-01','2023-01-28','O+','HINDU','Non-Vegetarian','Yes','11th',NULL,NULL,'Yes','E-839153','2006-04-25','COMDT 3 MTR','GOOD','GOOD',NULL,'Yes','AEMPT2703H',NULL,NULL,NULL,'20039881008','SBI','SBIN0007100','92/01','AYYANA PETA','9515263721','AYYANAPETA','VIZIANAGARAM','VIZIANAGARAM','VIZIANAGARAM','VIZIANAGARAM','VISHAKHAPATNAM','VIZIANGARAM','ANDHRA PRADESH',NULL,NULL,174.00,76.00,93.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,'Excellent','DHANA LAKSHMI','WIFE','2007-02-25','20039881008','SBI','SBIN0007100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 18:28:27','2026-02-04 14:48:39','1 Company',0,0,0,NULL,NULL,0,0,NULL,'CHQ'),(102,'DURGESH KHAROLE','15722524A','L HAV','LMN','2010-09-27','1991-09-09','2003-01-01','2023-02-07','A+','HINDU','Non-Vegetarian','Yes','B.A.',NULL,NULL,'Yes','F-168757','2011-04-19','COMDT 1 STC','GOOD','GOOD',NULL,'Yes','CHGPK3427E','0/0101/0039/2012','849254031720','0/0045/0004/2015','31532442853','SBI','SBIN0000318',NULL,'JAIPUR','6266171458','GARRA','GARRA','WARASEONI','WARASEONI','GONDIA','JABALPUR','BALAGHAT','MADHYA PRADESH','No',NULL,174.00,85.00,90.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','AVCHANA KHAROLE','WIFE','2017-02-28','31532442853','SBI','SBIN0000318',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 06:26:07','2026-01-27 06:26:07','1 Company',0,0,0,NULL,NULL,0,0,NULL,'CHQ'),(103,'RAVI KANT','15724706M','LOC NK','EFS','2011-03-14','1989-10-27','2025-04-09','2025-05-06','O+','HINDU','Vegetarian','Yes','12th',NULL,NULL,'Yes','G-065459','2022-03-21','COMDT 3 MTR',NULL,NULL,NULL,'Yes','BRNPK6538P','0/0690/0017/2013','602062386058','0/0037/0006/2016','20077103644','SBI','SBIN0005670',NULL,'LUHSANA','8399803853','BUDHANA','LUHSANA','BUDHANA','BUDHANA','MEERUT CANTT','MEERUT','MEZAFFARNAGAR','UTTAR PRADESH','No',NULL,176.00,81.00,86.00,'BLACK MOLE UPPER ASPECT',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','SONAM','WIFE','2013-04-04','20077103644','SBI','SBIN0005670','0/0309/0006/2020',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 06:50:22','2026-01-27 06:50:22','1 Company',0,0,0,NULL,NULL,0,0,NULL,'CHQ'),(104,'PRADEEP KUMAR NAHAK','A4203499F','Agniveer','TTC','2023-10-25','2003-02-28','2021-01-04','2024-06-20','O+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-387976','2023-12-05','COMDT-1 STC','EX','EX',NULL,'Yes','CQVPN7308H',NULL,'422434843107',NULL,'50100770139159','HDFC','HDFC0004229','L.N STREET 11th LINE','BERCHAMPUR','9438237465',NULL,'PANIGRAHIPENTHO','BADABAZAR','BERCHAMPUR','BERCHAMPUR','INS CHILKA','GANGAM','ODISHA',NULL,NULL,182.00,68.00,NULL,'0.5CM MOLE ON LT ARM',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','SUNATI NAHAK','MOTHER',NULL,'50100770139139','HDFC','HDFC0004229',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 06:58:38','2026-01-27 06:58:38','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','CHQ'),(105,'VIJAY PAL','A4204720F','Agniveer','CLK SD','2023-10-29','2003-06-25','2024-06-06','2024-06-21','A+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-346396','2023-12-20','COMDT 1 STC',NULL,NULL,NULL,'Yes',NULL,'5/04388/2023/17235001K',NULL,'5/04388/2023/1735001K',NULL,NULL,NULL,NULL,'LADPUR','9797067341','HARSORA','HARSORA','HARSORA','BANSUR','ALWAR','ALWAR','KOTPATTI BEHROR','RAJASTHAN',NULL,NULL,168.00,63.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 07:06:00','2026-01-27 07:06:00','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','CHQ'),(106,'ABHISHEK YADAV','A4207474M','Agniveer','CLK SD','2025-04-25','2004-01-24','2025-12-05','2026-01-04','B+','HINDU','Non-Vegetarian','No','GRADUATION (B.A.)',NULL,NULL,'Yes','G-524605','2025-06-10','COMDT 1STC','GOOD','EX',NULL,'Yes','BKSPY5978E',NULL,'520369826789',NULL,NULL,NULL,NULL,NULL,'SOKANI','9335797674','PURAINA','PURAINA','KARANDA','GHAZIPUR','ZAMANIA','VANARASI','GHAZIPUR','UTTAR PRADESH','No',NULL,163.00,52.00,78.00,'BM 1CM BELOW RT CLAVICLE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','SAVITA DEVI','MOTHER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 07:14:51','2026-01-27 07:14:51','1 Company',0,0,0,NULL,NULL,0,0,'Batch 6','CHQ'),(107,'MANOHAR KUMAR','15732973H','L HAV','LMN','2012-09-30','1992-06-15','2023-01-10','2023-02-10','O+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','F-515586','2013-03-02','COMDT 3 MTR','EX','GOOD','2024-10-22','Yes','DGVPK3051B','3/2535/0012/2013','546554774587','0/0040/0039/2015','35808701964','SBI','SBIN0000097',NULL,'SARARI','9149679319',NULL,'DAULATPUR','JAMUI','JAMUI','KIUL','DANAPUR','JAMUI','BIHAR','Yes',500.00,174.00,75.00,80.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','SUNITA KUMARI','WIFE','2015-05-31','35808701964','SBI','SBIN0000097',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 07:42:10','2026-01-27 07:42:10','1 Company',0,0,0,NULL,NULL,0,0,NULL,'LINE'),(108,'AMBRESH','A4205053L','Agniveer','LMN','2024-04-22','2004-04-21','2025-01-03','2025-01-08','B+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-493449','2024-06-26','COMDT 1STC','EX','EX',NULL,'Yes','EVCPA3698P',NULL,'275480184672',NULL,'20521555327','SBI','SBIN0016410',NULL,'PATTAN','9103811151','KALABURGI','PATTAN','SUB-URBAN','KALABURGI','KALABURGI','KALABURGI','KALABURGI','KARNATAKA','No',NULL,167.00,51.00,77.00,'BM OUTER ASPECT AT SHOULDER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','SAROJA','MOTHER',NULL,'20521555327','SBI','SBIN0016410',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 07:50:18','2026-01-27 07:50:18','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','LINE'),(109,'SUDISH KUMAR','15748339K','L NK','LMN','2016-04-03','1995-10-21','2022-09-01','2022-09-23','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-775561','2016-09-10','COMDT 3 MTR','EX','EX',NULL,'Yes','DJRPK7914N','3/0506/002/2016','266272495323','0/693/011/2017','35769538795','SBI','SBIN0005785',NULL,'KHABSI','9471210064','GAURA','KHABSI','BANIAPUR','SARAN','CHHAPRA','DANAPUR','SARAN','BIHAR',NULL,NULL,172.00,64.00,85.00,'A BLACK MOLE ON THE NOSE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','KIRAN KUMARI','WIFE','2019-05-19','35769538795','SBI','SBIN0005785','0/0486/025/2021',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 07:57:58','2026-01-27 07:57:58','1 Company',0,0,0,NULL,NULL,0,0,NULL,'LINE'),(110,'SUKHDEV','15736649H','L NK','LMN','2013-08-14','1995-03-15','2023-07-22','2023-08-26','AB+','HINDU','Non-Vegetarian','Yes','10th',NULL,NULL,'Yes','F-704287','2014-01-29','COMDT-1 STC','GOOD','GOOD','2025-04-04','Yes','FEJPS3419P',NULL,'663838757495',NULL,'33283007995','SBI','SBIN0001872','MISSION COMPOUND WARD NO 1','TANAKPUR','8871312108','TANAKPUR','TANAKPUR','TANAKPUR','PURNAGIRI','HALDWANI','DEHRADUN','CHAMPAWAT','UTTRAKHAND',NULL,NULL,172.00,85.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor','BHAWANA SHRIVASTAVA','WIFE','2021-11-21','33283007995','SBI','SBIN0001872','0/0364/0007/2024',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 08:07:27','2026-01-27 08:07:27','1 Company',0,0,0,NULL,NULL,0,0,NULL,'LINE'),(111,'PADIGELA RAMESH','15721376N','NK','LMN','2010-07-07','1992-06-17','2025-05-11','2025-07-21','O+','HINDU','Non-Vegetarian','Yes','10Tth',NULL,NULL,'Yes','F-168138','2011-01-19','COMDT-1 STC','GOOD','EX','2025-02-10','Yes','BBWPR2497C','0/0201/0015/2012','700438302253','0/0123/0008/2017','31419225851','SBI','SBIN0012966','2-122','PIPRI','9103113980','ADILABAD','PIPRI','BAZAR HATHNOOR','BAZAR HATHNOOR','ADILABAD','SECUNDERABAD','ADILABAD','TELANGANA',NULL,NULL,175.00,75.00,85.00,'BM ON RT SIDE OF NOSE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'P SUMALATHA','WIFE','2018-08-17','31419225851','SBI','SBIN0012966',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 08:16:06','2026-01-27 08:16:06','1 Company',0,0,0,NULL,NULL,0,0,NULL,'LINE'),(112,'UPPARA MADHU','A4204683Y','Agniveer','LMN','2023-10-23','2005-03-23','2024-06-06','2024-06-30','B+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-347074','2023-12-29','COMDT-1 STC','EX','EX',NULL,'Yes','IODPM9546C',NULL,'422117472823',NULL,'20511512410','SBI','SBIN0006305','29-6120B','KARLAKUNTA','6303137142','KURNOOL','JAGADURIHI','KRISHNAGIRI','KRISHNAGIRI','DHONE','SECUNDRABAD','KURNOOL','ANDHRA PRADESH',NULL,NULL,167.00,59.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'I JAYAMMA','MOTHER',NULL,'20511512410','SBI','SBIN0006305',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 08:31:00','2026-02-04 14:48:39','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','LINE'),(113,'ANIL CHALAWADI','A4204856L','Agniveer','LMN','2023-11-30','2003-05-05',NULL,NULL,'A+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-346430','2023-12-20','COMDT 1STC',NULL,NULL,NULL,NULL,'CTNPC0283M',NULL,'495091402500',NULL,'20511519051','SBI','SBIN0004452','ILAL BAGALKOT KARNATKA','ILAL','9103705324',NULL,'ILAL','BAGALKOT','BAGALKOT','BAGALKOT','BAGALKOT BENGLOR','BAGALKOT','KARNATAKA',NULL,NULL,168.00,57.00,80.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','SHANNKRAPPA','FATHER',NULL,'20511519051','SBI','SBIN0004452',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 11:27:01','2026-01-27 11:27:01','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','LINE'),(114,'AMAN KUMAR','A4203556X','Agniveer','LMN','2023-10-24','2003-01-03','2024-06-06','2024-06-17','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-346083','2023-12-14','COMDT 1STC','EX','EX',NULL,'Yes','LTRPK1546C',NULL,'320565818583',NULL,NULL,NULL,NULL,NULL,'KAWALANDH','8483048897','GOBINDPUR','GOBINDPUR','GOBINDPUR','GOBINDPUR','DHANBAD','RANCHI','DHANBAD','JHARKHAND','No',NULL,172.00,70.00,85.00,'BM FRONT OF NECK',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'BACHANI DEVI','MOTHER',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 11:34:05','2026-01-27 11:34:05','1 Company',0,0,0,NULL,NULL,0,0,'Batch 3','LINE'),(115,'HEMANTA DEY','A4205008Y','Agniveer','LMN','2024-04-21','2003-01-02','2024-12-05','2025-01-11','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-347997','2024-06-20','COMDT 1 STC','EX','EX',NULL,'Yes','IVVPD9900G',NULL,'397581281834',NULL,'50100710493956','HDFC','HDFC0000224',NULL,'BENAPURA','9103921488','ANGUA','ANGUA','DANTAN','KHARAGPUR','KHARAGPUR','KOLKATA','WEST MEDINIPUR','WEST BENGAL',NULL,NULL,180.00,63.00,85.00,'BM ON RT SIDE OF NECK',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor','Poor',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 11:40:24','2026-01-27 11:40:24','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','LINE'),(116,'PAWAR SANKET SANJAY','A4204930F','Agniveer','LMN','2024-04-21','2002-10-07','2024-12-04','2024-01-13','A+','HINDU','Non-Vegetarian','No','12TH',NULL,NULL,'Yes','G-493360','2024-06-26','COMDT 1STC','EX','EX',NULL,'Yes',NULL,NULL,'596274573465',NULL,'20521554913','SBI','SBIN0000452',NULL,'TIRAKWADI','9209086463',NULL,'SARWADI KH','PHALTAN RURAL','PHALTAN','PUNE','PUNE','SATARA','MAHARASTRA',NULL,NULL,172.00,62.00,85.00,'A BM INFRONT OF UPPER .3 OF LT ARM',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','PAWAR ANITA SANJAY','MOTHER',NULL,'20521554913','SBI','SBIN0000452',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 11:50:02','2026-01-27 11:50:02','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','LINE'),(117,'ASHISH KUMAR GUPTA','A4205213A','Agniveer','LMN','2024-04-24','2005-08-04','2024-12-04','2025-01-03','A+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-347635','2024-06-15','COMDT 1STC','EX','EX',NULL,'Yes','EIRPG5636M',NULL,'847830483179',NULL,'50100717854668','HDFC','HDFC0000224',NULL,'MAJHARIA','7051048039',NULL,'MAJHARIA','BUXAR','BUXAR','PATNA','DANAPUR','BUXAR','BIHAR','No',NULL,172.00,65.00,NULL,'A MOLE ON THE RIGHT HAND',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Poor',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 11:56:05','2026-01-27 11:56:05','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','LINE'),(118,'SAJAN','A4200365X','Agniveer','LMN','2022-12-24','2004-03-19','2025-04-06','2025-04-18','O+','HINDU','Vegetarian','No','10th',NULL,NULL,'Yes','G-105943','2003-03-01','COMDT 1STC','EX','EX',NULL,'Yes','PYIPS7508L',NULL,'435391253779',NULL,'41419147412','SBI','SBIN0010746','927','NAVROOP NAGAR','9041103532','BATALA','BATALA','AMRITSAR','PATHAN CANTT','AMRITSAR','PATHANCOAT','GURDASPUR','PUNJAB',NULL,NULL,174.00,64.00,85.00,'BM ON CHIN RIGHT SIDE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','MADANLAL ','FATHER',NULL,'41419147412','SBI','SBIN0010746',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 12:03:41','2026-01-27 12:03:41','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','LINE'),(119,'Majgaonkar Rushikesh Prakash','A4203007X','Agniveer','TCC','2023-03-14','2001-08-12','2025-08-20','2025-09-19','B+','HINDU','Non-Vegetarian','No','12th',NULL,NULL,'Yes','G-238327','2023-04-18','1 MTR',NULL,NULL,NULL,'Yes','HDSPM1790M','5/02760/2023/1735001K','498800551934','5/02760/2023/1735001K','20511507953','SBI','SBIN0006587','103','SHIROLI PULACHI','8600861192',NULL,'SHIROLI MIDC','SHIROLI MIDC','HATKANANGALE','KOLHAPUR','PUNE','KOLHAPUR','MAHARASHTRA','No',NULL,170.00,65.00,85.00,'BM 7CM LT OF ADAM APPLE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 14:29:37','2026-01-27 14:29:37','1 Company',0,0,0,NULL,NULL,0,0,'Batch 2','MW'),(121,'SHUBHAM','A4205888A','Agniveer','LMN','2024-04-27','2005-07-15','2024-12-03','2025-01-03','O+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-493748','2024-06-29','COMDT-1 STC','EX','EX',NULL,'Yes',NULL,NULL,'702181974206',NULL,'2113000100252191','PNB','PUNB0211300',NULL,'TANDAWA SHUKLA','9120665039',NULL,'TANDAWA BHARATPUR','RAJESULTANPUR','ALLAPUR','AKBERPUR','LUCKNOW','AMBEDKER NAGAR','UTTAR PRADESH','No',NULL,174.00,58.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 07:35:42','2026-01-28 07:35:42','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','LINE'),(122,'RAUT PANKAJ J','15749159N','L NK','LMN','2016-06-10','1996-11-16','2022-08-20','2022-09-15','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-820272','2016-11-13','COMDT 3 MTR','EX','EX',NULL,'Yes','CEVPR0348D','3/0664/0022/2016','683957183597','0/0038/0003/2014','38659786253','SBI','SBIN0000563',NULL,'FETRI','7025645825','KATOL','KHANGUON','KATOL','KATOL','KATOL','NAGPUR','NAGPUR','MAHARASHTRA',NULL,NULL,170.00,76.00,86.00,'BM MID .3 LT ARM',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'BABUBAI RAUT','MOTHER',NULL,'38659786253','SBI','SBIN0000563','0/1099/0007/2019',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 07:41:58','2026-01-28 07:41:58','1 Company',0,0,0,NULL,NULL,0,0,NULL,'LINE'),(123,'HARIBALA S','A4206051M','Agniveer','LMN','2024-04-24','2003-02-02','2024-01-24','2024-12-03','A+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-347549',NULL,NULL,'EX','EX',NULL,NULL,'QFCPS0212H',NULL,'706273590469',NULL,'246401505394','ICICI',NULL,'W3/35','PALLAUARAYANPATTI','9345824844','UTHAMAPALAYAM','PANNIPURAM','KOMBAI','UTHAMAPALAYAM','MADURAI','EOIMBATOUR','THENI','TAMILNADU',NULL,NULL,170.00,54.00,182.00,'BM 4CM BELOW MIDDLE .3 RD LT COLLAR BONE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 07:49:36','2026-01-28 07:49:36','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','LINE'),(124,'G SREENIVASULU','15715916L','HAV','TTC','2009-06-26','1990-04-05','2022-12-31','2023-02-07','O+','HINDU','Non-Vegetarian','Yes','12th',NULL,NULL,'Yes','F-165286','2009-11-26','COMDT 1 STC','EX','EX',NULL,'Yes','BDOPG6955Q',NULL,'648608369996',NULL,'30901523923','SBI','SBIN0000986','2-33/1','JUFUR','8464888535','PATULAPADU','JUTUR','PATULAPADU','PATULAPADU','KURNOOL','SEEMIABAD','KURNOOL','ANDHRA PRADESH',NULL,NULL,180.00,74.00,85.00,'BLACK MOLE ON THE RIGHT HAND',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Excellent','G SRILATHA','WIFE','2018-04-18','30901523920','SBI','SBIN0000986',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 11:09:01','2026-02-04 14:48:39','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(125,'SATYENDRA SINGH','15742217K','L NK','TTC','2015-04-02','1996-06-05','2022-12-03','2023-12-09','AB+','HINDU','Non-Vegetarian','Yes','12th',NULL,NULL,'Yes','F-713826','2015-11-04','COMDT 3 MTR','EX','EX',NULL,'Yes','GCAPS6846G','3/2278/0006/2016','258511468623','3/2278/0012/2016','34891609480','SBI','SBIN0012996',NULL,'HADHUA','6005052132','GHOSI','GHOSI','GHOSI','GHOSI','MAU','GORAKHPUR','MAU','UTTAR PRADESH','No',NULL,173.00,82.00,88.00,'A BM UPPER RT ELBOW',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,'Excellent','HARSHITA SINGH','WIFE','2022-02-10','34891609480','SBI','SBIN0012966',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 11:16:29','2026-01-28 11:16:29','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(126,'SUDHIR KUMAR','15756017Y','Signal Man','TTC','2018-05-30','1999-08-16','2025-09-26','2025-10-05','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-996927','2018-11-20','COMDT 3 MTR','GOOD','GOOD','2024-12-23','Yes','GMNPK8510A','3/2117/0003/2019','543758803557','3/0542/0003/2020','6449000100024033','PNB','PUNB0064900',NULL,'NAGLA ANI','7830225137','BARDWARI','BARDWARI','MURSAN','HATHRAS','MURSAN','MATHURA','HATHRAS','UTTAR PRADESH',NULL,NULL,175.00,86.00,84.00,'A MOLE ON LEFT CHEEK',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','NISHA CHOUDHARI','WIFE','2022-04-20','6449000100024053','PNB','PUNB0064900','0/0405/0015/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 11:24:13','2026-02-02 14:49:17','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(127,'RAHUL LAGAD D','A4205388H','Agniveer','TTC','2024-04-24','2004-08-22','2024-12-03','2025-01-02','B+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','G-347820','2024-01-18','COMDT-1 STC','EX','EX','2025-08-08','Yes','BRVPL7172F',NULL,'551421767421',NULL,'50100721490096','HDFC','HDFC0002544','09','ADHARWAD','8899330452','IGATPURI','KHED','GHOTI BK','IGATPURI','NASHIK ROAD','NASHIK ROAD','NASHIK','MAHARASHTRA','No',NULL,168.00,56.00,78.00,'0.5CM MOLE ON CHEST',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent','Poor','MANISHA D.L.','MOTHER',NULL,'50100721490096','HDFC','HDFC0002544',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 11:30:48','2026-01-28 11:30:48','1 Company',0,0,0,NULL,NULL,0,0,'Batch 4','MW'),(128,'ABHISHEK KUMAR YADAV','15752536K','Signal Man','TTC','2017-03-19','1997-06-05',NULL,NULL,'A+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-991707','2017-09-16','COMDT-1STC',NULL,'EX',NULL,NULL,'ANDPY0250C',NULL,NULL,NULL,'20432012563','SBI','SBIN0009915',NULL,'SARAIYAN PRAVESHPUR','7860471110',NULL,'SHEKHPUR ASHIQ','HATHIGAWAN','KUNDA','PRAYAGRAJ JN','PRAYAGRAJ','PRATAPGARH','UTTAR PRADESH','No',NULL,168.00,65.50,NULL,'A BLACK MOLE RIGHT CHEECK BONE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'SAVITA YADAV','WIFE','2022-05-02','20432012563','SBI','SBIN0009915',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 11:36:37','2026-01-28 11:36:37','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(129,'SWAPANIR KUMAR','15706852K','Signal Man','TTC','2006-12-12','1986-07-05','2025-10-24','2025-11-07','AB+','HINDU','Vegetarian','No','12th',NULL,NULL,'Yes','F-712937','2015-06-27','COMDT 3MTR','EX','EX',NULL,'No','BMBPK1603D','0/0046/0016/2012','422526578375','0/0422/0019/2015','50100774011260','HDFC',NULL,NULL,'PIMMA MIWADA','7901732919','KANPUR','KARWAN','RASULABAD','RASULABAD','BILHAUR','KANPUR','KANPUR DEHAT','UTTAR PRADESH','No',NULL,173.00,71.00,80.00,'A BM ON NOSE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'KALPANA DEVI','WIFE','2012-02-15','50100774011260','HDFC',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 11:42:27','2026-01-28 11:42:27','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(130,'ASHISH SINGH','A4350867L','Agniveer','OCC','2022-12-25','2004-05-05','2025-04-05','2025-04-19','AB+','HINDU','Vegetarian','No','12tH',NULL,NULL,'Yes','G-075064','2023-03-02','COMDT 3 MTR','EX','EX','2025-03-20','Yes','PGEPS6109L',NULL,'456484428529',NULL,'41549428871','SBI','SBIN0007936','21/SAMVANSHI HOUSE','CHOOND KHURD','8825020847','JAITWARA','JAITWARA','KOTAR','KOTAR','SATNA JN','JABALPUR','SATNA','MADHYA PRADESH','No',NULL,176.00,67.00,84.00,'MOLE ON LEFT CHEST',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,'Excellent',NULL,'SUNITA SINGH','MOTHER',NULL,'41549428871','SBI','SBIN0007936',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 12:25:29','2026-01-28 12:25:29','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','OP'),(131,'AMRENDRA SHUKLA ','15744564F','L NK','TTC','2015-10-16','1994-07-15','2025-09-30','2025-10-30','B+','HINDU','Vegetarian','No',NULL,NULL,NULL,'Yes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'UTTAR PRADESH',NULL,NULL,185.00,80.00,90.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-06 06:54:42','2026-02-06 06:54:42','HQ company',0,0,0,NULL,NULL,0,0,NULL,'RHQ'),(132,'PUSHPENDRA','15734024P','HAV','LMN','2013-02-21','1991-12-20','2025-12-31','2026-02-06','A+','HINDU','Non-Vegetarian','Yes',NULL,NULL,NULL,'No','F585512','2013-08-01','3 MTR','EX','EX',NULL,NULL,'DNAPK5960H',NULL,'379307565546',NULL,'32946979779','SBI','SBIN0008599','HNO 36',NULL,'7759077599',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'BIHAR',NULL,NULL,178.00,79.00,90.00,'BM OVER RT NIPPLE AT 1  CLOCK',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-13 07:57:18','2026-02-13 08:39:00','1 Company',0,0,0,NULL,NULL,0,0,NULL,'MW'),(133,'CODER','12345t','Agniveer','ttc','2024-06-15','2000-10-11','2026-02-01','2026-02-04','A+','hindu','Vegetarian','No',NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0/2233/33/100/2025',NULL,NULL,'72688729777229','SBI','SBIN0018282',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'KERALA',NULL,NULL,178.00,78.00,76.00,NULL,NULL,NULL,72,NULL,NULL,NULL,NULL,NULL,'4 MONTHS',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-13 08:08:21','2026-02-13 08:08:21','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','IT'),(135,'CODERWW','12345EE','Agniveer','ttc','2024-06-15','2000-10-11','2026-02-01','2026-02-04','A+','hindu','Vegetarian','No',NULL,NULL,NULL,'No',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0/2233/33/100/2025',NULL,NULL,'72688729777229','SBI','SBIN0018282',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'KERALA',NULL,NULL,178.00,78.00,76.00,NULL,NULL,NULL,72,NULL,NULL,NULL,NULL,NULL,'4 MONTHS',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-13 08:09:35','2026-02-13 08:09:35','1 Company',0,0,0,NULL,NULL,0,0,'Batch 1','IT');
/*!40000 ALTER TABLE `personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personnel_sports`
--

DROP TABLE IF EXISTS `personnel_sports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnel_sports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(50) NOT NULL,
  `sport_type` varchar(50) NOT NULL,
  `sport_name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personnel_sports`
--

LOCK TABLES `personnel_sports` WRITE;
/*!40000 ALTER TABLE `personnel_sports` DISABLE KEYS */;
/*!40000 ALTER TABLE `personnel_sports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posting_details_table`
--

DROP TABLE IF EXISTS `posting_details_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posting_details_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(15) NOT NULL,
  `location_posted_to` varchar(10) NOT NULL,
  `posting_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `army_number` (`army_number`),
  CONSTRAINT `posting_details_table_ibfk_1` FOREIGN KEY (`army_number`) REFERENCES `personnel` (`army_number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posting_details_table`
--

LOCK TABLES `posting_details_table` WRITE;
/*!40000 ALTER TABLE `posting_details_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `posting_details_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_heads`
--

DROP TABLE IF EXISTS `project_heads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_heads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `head_name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `head_name` (`head_name`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_heads`
--

LOCK TABLES `project_heads` WRITE;
/*!40000 ALTER TABLE `project_heads` DISABLE KEYS */;
INSERT INTO `project_heads` VALUES (7,'OCPP','2026-01-21 12:36:45'),(8,'TAG','2026-01-21 12:37:03'),(9,'SRE','2026-01-21 12:37:12'),(10,'IT HARDWARE','2026-01-21 12:37:23'),(11,'IT SOFTWARE','2026-01-21 12:37:36'),(12,'SAG','2026-01-21 12:37:49');
/*!40000 ALTER TABLE `project_heads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_history`
--

DROP TABLE IF EXISTS `project_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_history` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `stage` varchar(100) NOT NULL,
  `notes` text,
  `updated_by` varchar(200) DEFAULT NULL,
  `updated_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`history_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `project_history_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_history`
--

LOCK TABLES `project_history` WRITE;
/*!40000 ALTER TABLE `project_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) NOT NULL,
  `current_stage` varchar(255) DEFAULT NULL,
  `project_cost` decimal(10,2) DEFAULT NULL,
  `project_items` varchar(255) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `project_description` text,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `head` varchar(100) NOT NULL,
  `company` varchar(50) DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(200) DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Active',
  PRIMARY KEY (`project_id`),
  KEY `idx_projects_company` (`company`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (5,'trg','B BD',300000.00,'\"laptops \"',234,'','2026-01-25 01:56:06','IT HARDWARE','HQ company',NULL,NULL,NULL,'Active'),(6,'REPAIR OF POWER EQPTS OUT OF TAG IN 15 CORPS Z','Payment',200000.00,'\"UPS AND OTHER POWER SUPPLY EQPT\"',100,'','2026-02-03 10:21:41','TAG','Admin','2026-02-11 13:18:23',NULL,NULL,'Active');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `punishments`
--

DROP TABLE IF EXISTS `punishments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `punishments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `punishment_date` date DEFAULT NULL,
  `punishment` varchar(255) DEFAULT NULL,
  `aa_sec` varchar(100) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_punishments` (`personnel_id`),
  CONSTRAINT `punishments_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `punishments`
--

LOCK TABLES `punishments` WRITE;
/*!40000 ALTER TABLE `punishments` DISABLE KEYS */;
INSERT INTO `punishments` VALUES (23,40,'15720341L',1,'2024-05-15','RED','63',''),(24,135,'12345EE',1,'2026-02-01','RED','148A','93893893883');
/*!40000 ALTER TABLE `punishments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roll_call_points`
--

DROP TABLE IF EXISTS `roll_call_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roll_call_points` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(20) NOT NULL,
  `point_title` varchar(100) NOT NULL,
  `point_description` text NOT NULL,
  `army_number` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rollcall_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roll_call_points`
--

LOCK TABLES `roll_call_points` WRITE;
/*!40000 ALTER TABLE `roll_call_points` DISABLE KEYS */;
INSERT INTO `roll_call_points` VALUES (7,'OR_REQUEST','Medical Assistance','required','15753860N','2026-02-05 03:52:52','PENDING'),(8,'OR_REQUEST','Medical Assistance','done','15720341L','2026-02-05 03:54:07','PENDING'),(9,'SM_SUGGESTION','Training Improvement','PLS IMMPLEMENT',NULL,'2026-02-05 07:13:14',NULL),(10,'SM_SUGGESTION','Discipline & Conduct','MT ACCIDENT  IS A OFFANCIVE CRIME',NULL,'2026-02-05 08:43:29',NULL),(11,'OR_REQUEST','Equipment Requirement','LAYOUT 3 AND 4 LAPTOP IN TRH LAB FOR PRACTICE','15719951l','2026-02-05 08:51:12','PENDING'),(12,'SM_SUGGESTION','Training Improvement','sqssss',NULL,'2026-02-05 09:50:44','SUGGESTED'),(13,'OR_REQUEST','Leave / Pass Request','done','15719951l','2026-02-07 14:04:23','PENDING');
/*!40000 ALTER TABLE `roll_call_points` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `liquor_sale` int NOT NULL,
  `grocery_sale` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensitive_marking`
--

DROP TABLE IF EXISTS `sensitive_marking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensitive_marking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(100) DEFAULT NULL,
  `reason` text,
  `marked_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensitive_marking`
--

LOCK TABLES `sensitive_marking` WRITE;
/*!40000 ALTER TABLE `sensitive_marking` DISABLE KEYS */;
INSERT INTO `sensitive_marking` VALUES (26,'15744564F','My school is a place of learning, discipline, and growth. It','2026-02-17 12:58:01');
/*!40000 ALTER TABLE `sensitive_marking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_items`
--

DROP TABLE IF EXISTS `store_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `store_id` int DEFAULT NULL,
  `qlp_no` varchar(50) DEFAULT NULL,
  `slp_no` varchar(50) DEFAULT NULL,
  `nomenclature` varchar(200) DEFAULT NULL,
  `au` varchar(20) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `store_id` (`store_id`),
  CONSTRAINT `store_items_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `stores` (`store_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_items`
--

LOCK TABLES `store_items` WRITE;
/*!40000 ALTER TABLE `store_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stores`
--

DROP TABLE IF EXISTS `stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stores` (
  `store_id` int NOT NULL AUTO_INCREMENT,
  `store_name` varchar(100) NOT NULL,
  `place` varchar(100) DEFAULT NULL,
  `incharge_name` varchar(100) DEFAULT NULL,
  `total_items` int DEFAULT '0',
  PRIMARY KEY (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stores`
--

LOCK TABLES `stores` WRITE;
/*!40000 ALTER TABLE `stores` DISABLE KEYS */;
/*!40000 ALTER TABLE `stores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(200) NOT NULL,
  `description` text,
  `priority` varchar(10) DEFAULT 'medium',
  `assigned_to` varchar(255) DEFAULT NULL,
  `assigned_by` varchar(255) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `task_status` varchar(40) DEFAULT 'Pending',
  `remarks` varchar(100) DEFAULT 'No Remarks',
  `range_status` tinyint DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_tasks_assigned_status` (`assigned_to`,`task_status`),
  CONSTRAINT `tasks_chk_1` CHECK ((`priority` in (_utf8mb4'low',_utf8mb4'medium',_utf8mb4'high',_utf8mb4'urgent')))
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (23,'UMS hosting','TILL ','High','jc393919L','CO','2026-01-27','2026-01-27 13:55:53','In Progress','WORK IN PROGRESS',36),(24,'Conduct VIP visit','contact to concern officer and report timely','High','jc393919L','CO','2026-02-27','2026-02-09 12:37:24','Pending','No Remarks',0);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `td_table`
--

DROP TABLE IF EXISTS `td_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `td_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(50) NOT NULL,
  `remarks` text,
  `td_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `company` varchar(50) DEFAULT NULL,
  `authority` varchar(50) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `td_table`
--

LOCK TABLES `td_table` WRITE;
/*!40000 ALTER TABLE `td_table` DISABLE KEYS */;
INSERT INTO `td_table` VALUES (10,'157606852K','Location: DELHI, Authority: ADJT','2026-02-11 11:31:50','1 Company','ADJT','DELHI');
/*!40000 ALTER TABLE `td_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_manpower_daily`
--

DROP TABLE IF EXISTS `trade_manpower_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_manpower_daily` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_date` date NOT NULL,
  `op_ciph_auth` int DEFAULT '0',
  `op_ciph_hs` int DEFAULT '0',
  `op_ciph_held` int DEFAULT '0',
  `op_ciph_av` int DEFAULT '0',
  `op_ciph_dist_hq` int DEFAULT '0',
  `op_ciph_dist_1` int DEFAULT '0',
  `op_ciph_dist_2` int DEFAULT '0',
  `op_ciph_dist_3` int DEFAULT '0',
  `op_ciph_state_hq` int DEFAULT '0',
  `op_ciph_state_1` int DEFAULT '0',
  `op_ciph_state_2` int DEFAULT '0',
  `op_ciph_state_3` int DEFAULT '0',
  `op_ciph_present_hq` int DEFAULT '0',
  `op_ciph_present_1` int DEFAULT '0',
  `op_ciph_present_2` int DEFAULT '0',
  `op_ciph_present_3` int DEFAULT '0',
  `oss_auth` int DEFAULT '0',
  `oss_hs` int DEFAULT '0',
  `oss_held` int DEFAULT '0',
  `oss_av` int DEFAULT '0',
  `oss_dist_hq` int DEFAULT '0',
  `oss_dist_1` int DEFAULT '0',
  `oss_dist_2` int DEFAULT '0',
  `oss_dist_3` int DEFAULT '0',
  `oss_state_hq` int DEFAULT '0',
  `oss_state_1` int DEFAULT '0',
  `oss_state_2` int DEFAULT '0',
  `oss_state_3` int DEFAULT '0',
  `oss_present_hq` int DEFAULT '0',
  `oss_present_1` int DEFAULT '0',
  `oss_present_2` int DEFAULT '0',
  `oss_present_3` int DEFAULT '0',
  `occ_auth` int DEFAULT '0',
  `occ_hs` int DEFAULT '0',
  `occ_held` int DEFAULT '0',
  `occ_av` int DEFAULT '0',
  `occ_dist_hq` int DEFAULT '0',
  `occ_dist_1` int DEFAULT '0',
  `occ_dist_2` int DEFAULT '0',
  `occ_dist_3` int DEFAULT '0',
  `occ_state_hq` int DEFAULT '0',
  `occ_state_1` int DEFAULT '0',
  `occ_state_2` int DEFAULT '0',
  `occ_state_3` int DEFAULT '0',
  `occ_present_hq` int DEFAULT '0',
  `occ_present_1` int DEFAULT '0',
  `occ_present_2` int DEFAULT '0',
  `occ_present_3` int DEFAULT '0',
  `ttc_auth` int DEFAULT '0',
  `ttc_hs` int DEFAULT '0',
  `ttc_held` int DEFAULT '0',
  `ttc_av` int DEFAULT '0',
  `ttc_dist_hq` int DEFAULT '0',
  `ttc_dist_1` int DEFAULT '0',
  `ttc_dist_2` int DEFAULT '0',
  `ttc_dist_3` int DEFAULT '0',
  `ttc_state_hq` int DEFAULT '0',
  `ttc_state_1` int DEFAULT '0',
  `ttc_state_2` int DEFAULT '0',
  `ttc_state_3` int DEFAULT '0',
  `ttc_present_hq` int DEFAULT '0',
  `ttc_present_1` int DEFAULT '0',
  `ttc_present_2` int DEFAULT '0',
  `ttc_present_3` int DEFAULT '0',
  `lmn_auth` int DEFAULT '0',
  `lmn_hs` int DEFAULT '0',
  `lmn_held` int DEFAULT '0',
  `lmn_av` int DEFAULT '0',
  `lmn_dist_hq` int DEFAULT '0',
  `lmn_dist_1` int DEFAULT '0',
  `lmn_dist_2` int DEFAULT '0',
  `lmn_dist_3` int DEFAULT '0',
  `lmn_state_hq` int DEFAULT '0',
  `lmn_state_1` int DEFAULT '0',
  `lmn_state_2` int DEFAULT '0',
  `lmn_state_3` int DEFAULT '0',
  `lmn_present_hq` int DEFAULT '0',
  `lmn_present_1` int DEFAULT '0',
  `lmn_present_2` int DEFAULT '0',
  `lmn_present_3` int DEFAULT '0',
  `efs_auth` int DEFAULT '0',
  `efs_hs` int DEFAULT '0',
  `efs_held` int DEFAULT '0',
  `efs_av` int DEFAULT '0',
  `efs_dist_hq` int DEFAULT '0',
  `efs_dist_1` int DEFAULT '0',
  `efs_dist_2` int DEFAULT '0',
  `efs_dist_3` int DEFAULT '0',
  `efs_state_hq` int DEFAULT '0',
  `efs_state_1` int DEFAULT '0',
  `efs_state_2` int DEFAULT '0',
  `efs_state_3` int DEFAULT '0',
  `efs_present_hq` int DEFAULT '0',
  `efs_present_1` int DEFAULT '0',
  `efs_present_2` int DEFAULT '0',
  `efs_present_3` int DEFAULT '0',
  `dvr_mt_auth` int DEFAULT '0',
  `dvr_mt_hs` int DEFAULT '0',
  `dvr_mt_held` int DEFAULT '0',
  `dvr_mt_av` int DEFAULT '0',
  `dvr_mt_dist_hq` int DEFAULT '0',
  `dvr_mt_dist_1` int DEFAULT '0',
  `dvr_mt_dist_2` int DEFAULT '0',
  `dvr_mt_dist_3` int DEFAULT '0',
  `dvr_mt_state_hq` int DEFAULT '0',
  `dvr_mt_state_1` int DEFAULT '0',
  `dvr_mt_state_2` int DEFAULT '0',
  `dvr_mt_state_3` int DEFAULT '0',
  `dvr_mt_present_hq` int DEFAULT '0',
  `dvr_mt_present_1` int DEFAULT '0',
  `dvr_mt_present_2` int DEFAULT '0',
  `dvr_mt_present_3` int DEFAULT '0',
  `dr_auth` int DEFAULT '0',
  `dr_hs` int DEFAULT '0',
  `dr_held` int DEFAULT '0',
  `dr_av` int DEFAULT '0',
  `dr_dist_hq` int DEFAULT '0',
  `dr_dist_1` int DEFAULT '0',
  `dr_dist_2` int DEFAULT '0',
  `dr_dist_3` int DEFAULT '0',
  `dr_state_hq` int DEFAULT '0',
  `dr_state_1` int DEFAULT '0',
  `dr_state_2` int DEFAULT '0',
  `dr_state_3` int DEFAULT '0',
  `dr_present_hq` int DEFAULT '0',
  `dr_present_1` int DEFAULT '0',
  `dr_present_2` int DEFAULT '0',
  `dr_present_3` int DEFAULT '0',
  `dtmn_auth` int DEFAULT '0',
  `dtmn_hs` int DEFAULT '0',
  `dtmn_held` int DEFAULT '0',
  `dtmn_av` int DEFAULT '0',
  `dtmn_dist_hq` int DEFAULT '0',
  `dtmn_dist_1` int DEFAULT '0',
  `dtmn_dist_2` int DEFAULT '0',
  `dtmn_dist_3` int DEFAULT '0',
  `dtmn_state_hq` int DEFAULT '0',
  `dtmn_state_1` int DEFAULT '0',
  `dtmn_state_2` int DEFAULT '0',
  `dtmn_state_3` int DEFAULT '0',
  `dtmn_present_hq` int DEFAULT '0',
  `dtmn_present_1` int DEFAULT '0',
  `dtmn_present_2` int DEFAULT '0',
  `dtmn_present_3` int DEFAULT '0',
  `skt_auth` int DEFAULT '0',
  `skt_hs` int DEFAULT '0',
  `skt_held` int DEFAULT '0',
  `skt_av` int DEFAULT '0',
  `skt_dist_hq` int DEFAULT '0',
  `skt_dist_1` int DEFAULT '0',
  `skt_dist_2` int DEFAULT '0',
  `skt_dist_3` int DEFAULT '0',
  `skt_state_hq` int DEFAULT '0',
  `skt_state_1` int DEFAULT '0',
  `skt_state_2` int DEFAULT '0',
  `skt_state_3` int DEFAULT '0',
  `skt_present_hq` int DEFAULT '0',
  `skt_present_1` int DEFAULT '0',
  `skt_present_2` int DEFAULT '0',
  `skt_present_3` int DEFAULT '0',
  `artsn_auth` int DEFAULT '0',
  `artsn_hs` int DEFAULT '0',
  `artsn_held` int DEFAULT '0',
  `artsn_av` int DEFAULT '0',
  `artsn_dist_hq` int DEFAULT '0',
  `artsn_dist_1` int DEFAULT '0',
  `artsn_dist_2` int DEFAULT '0',
  `artsn_dist_3` int DEFAULT '0',
  `artsn_state_hq` int DEFAULT '0',
  `artsn_state_1` int DEFAULT '0',
  `artsn_state_2` int DEFAULT '0',
  `artsn_state_3` int DEFAULT '0',
  `artsn_present_hq` int DEFAULT '0',
  `artsn_present_1` int DEFAULT '0',
  `artsn_present_2` int DEFAULT '0',
  `artsn_present_3` int DEFAULT '0',
  `w_man_auth` int DEFAULT '0',
  `w_man_hs` int DEFAULT '0',
  `w_man_held` int DEFAULT '0',
  `w_man_av` int DEFAULT '0',
  `w_man_dist_hq` int DEFAULT '0',
  `w_man_dist_1` int DEFAULT '0',
  `w_man_dist_2` int DEFAULT '0',
  `w_man_dist_3` int DEFAULT '0',
  `w_man_state_hq` int DEFAULT '0',
  `w_man_state_1` int DEFAULT '0',
  `w_man_state_2` int DEFAULT '0',
  `w_man_state_3` int DEFAULT '0',
  `w_man_present_hq` int DEFAULT '0',
  `w_man_present_1` int DEFAULT '0',
  `w_man_present_2` int DEFAULT '0',
  `w_man_present_3` int DEFAULT '0',
  `steward_auth` int DEFAULT '0',
  `steward_hs` int DEFAULT '0',
  `steward_held` int DEFAULT '0',
  `steward_av` int DEFAULT '0',
  `steward_dist_hq` int DEFAULT '0',
  `steward_dist_1` int DEFAULT '0',
  `steward_dist_2` int DEFAULT '0',
  `steward_dist_3` int DEFAULT '0',
  `steward_state_hq` int DEFAULT '0',
  `steward_state_1` int DEFAULT '0',
  `steward_state_2` int DEFAULT '0',
  `steward_state_3` int DEFAULT '0',
  `steward_present_hq` int DEFAULT '0',
  `steward_present_1` int DEFAULT '0',
  `steward_present_2` int DEFAULT '0',
  `steward_present_3` int DEFAULT '0',
  `dresser_auth` int DEFAULT '0',
  `dresser_hs` int DEFAULT '0',
  `dresser_held` int DEFAULT '0',
  `dresser_av` int DEFAULT '0',
  `dresser_dist_hq` int DEFAULT '0',
  `dresser_dist_1` int DEFAULT '0',
  `dresser_dist_2` int DEFAULT '0',
  `dresser_dist_3` int DEFAULT '0',
  `dresser_state_hq` int DEFAULT '0',
  `dresser_state_1` int DEFAULT '0',
  `dresser_state_2` int DEFAULT '0',
  `dresser_state_3` int DEFAULT '0',
  `dresser_present_hq` int DEFAULT '0',
  `dresser_present_1` int DEFAULT '0',
  `dresser_present_2` int DEFAULT '0',
  `dresser_present_3` int DEFAULT '0',
  `hkeeper_auth` int DEFAULT '0',
  `hkeeper_hs` int DEFAULT '0',
  `hkeeper_held` int DEFAULT '0',
  `hkeeper_av` int DEFAULT '0',
  `hkeeper_dist_hq` int DEFAULT '0',
  `hkeeper_dist_1` int DEFAULT '0',
  `hkeeper_dist_2` int DEFAULT '0',
  `hkeeper_dist_3` int DEFAULT '0',
  `hkeeper_state_hq` int DEFAULT '0',
  `hkeeper_state_1` int DEFAULT '0',
  `hkeeper_state_2` int DEFAULT '0',
  `hkeeper_state_3` int DEFAULT '0',
  `hkeeper_present_hq` int DEFAULT '0',
  `hkeeper_present_1` int DEFAULT '0',
  `hkeeper_present_2` int DEFAULT '0',
  `hkeeper_present_3` int DEFAULT '0',
  `mkeeper_auth` int DEFAULT '0',
  `mkeeper_hs` int DEFAULT '0',
  `mkeeper_held` int DEFAULT '0',
  `mkeeper_av` int DEFAULT '0',
  `mkeeper_dist_hq` int DEFAULT '0',
  `mkeeper_dist_1` int DEFAULT '0',
  `mkeeper_dist_2` int DEFAULT '0',
  `mkeeper_dist_3` int DEFAULT '0',
  `mkeeper_state_hq` int DEFAULT '0',
  `mkeeper_state_1` int DEFAULT '0',
  `mkeeper_state_2` int DEFAULT '0',
  `mkeeper_state_3` int DEFAULT '0',
  `mkeeper_present_hq` int DEFAULT '0',
  `mkeeper_present_1` int DEFAULT '0',
  `mkeeper_present_2` int DEFAULT '0',
  `mkeeper_present_3` int DEFAULT '0',
  `chef_mess_auth` int DEFAULT '0',
  `chef_mess_hs` int DEFAULT '0',
  `chef_mess_held` int DEFAULT '0',
  `chef_mess_av` int DEFAULT '0',
  `chef_mess_dist_hq` int DEFAULT '0',
  `chef_mess_dist_1` int DEFAULT '0',
  `chef_mess_dist_2` int DEFAULT '0',
  `chef_mess_dist_3` int DEFAULT '0',
  `chef_mess_state_hq` int DEFAULT '0',
  `chef_mess_state_1` int DEFAULT '0',
  `chef_mess_state_2` int DEFAULT '0',
  `chef_mess_state_3` int DEFAULT '0',
  `chef_mess_present_hq` int DEFAULT '0',
  `chef_mess_present_1` int DEFAULT '0',
  `chef_mess_present_2` int DEFAULT '0',
  `chef_mess_present_3` int DEFAULT '0',
  `chef_com_auth` int DEFAULT '0',
  `chef_com_hs` int DEFAULT '0',
  `chef_com_held` int DEFAULT '0',
  `chef_com_av` int DEFAULT '0',
  `chef_com_dist_hq` int DEFAULT '0',
  `chef_com_dist_1` int DEFAULT '0',
  `chef_com_dist_2` int DEFAULT '0',
  `chef_com_dist_3` int DEFAULT '0',
  `chef_com_state_hq` int DEFAULT '0',
  `chef_com_state_1` int DEFAULT '0',
  `chef_com_state_2` int DEFAULT '0',
  `chef_com_state_3` int DEFAULT '0',
  `chef_com_present_hq` int DEFAULT '0',
  `chef_com_present_1` int DEFAULT '0',
  `chef_com_present_2` int DEFAULT '0',
  `chef_com_present_3` int DEFAULT '0',
  `er_auth` int DEFAULT '0',
  `er_hs` int DEFAULT '0',
  `er_held` int DEFAULT '0',
  `er_av` int DEFAULT '0',
  `er_dist_hq` int DEFAULT '0',
  `er_dist_1` int DEFAULT '0',
  `er_dist_2` int DEFAULT '0',
  `er_dist_3` int DEFAULT '0',
  `er_state_hq` int DEFAULT '0',
  `er_state_1` int DEFAULT '0',
  `er_state_2` int DEFAULT '0',
  `er_state_3` int DEFAULT '0',
  `er_present_hq` int DEFAULT '0',
  `er_present_1` int DEFAULT '0',
  `er_present_2` int DEFAULT '0',
  `er_present_3` int DEFAULT '0',
  `tlr_auth` int DEFAULT '0',
  `tlr_hs` int DEFAULT '0',
  `tlr_held` int DEFAULT '0',
  `tlr_av` int DEFAULT '0',
  `tlr_dist_hq` int DEFAULT '0',
  `tlr_dist_1` int DEFAULT '0',
  `tlr_dist_2` int DEFAULT '0',
  `tlr_dist_3` int DEFAULT '0',
  `tlr_state_hq` int DEFAULT '0',
  `tlr_state_1` int DEFAULT '0',
  `tlr_state_2` int DEFAULT '0',
  `tlr_state_3` int DEFAULT '0',
  `tlr_present_hq` int DEFAULT '0',
  `tlr_present_1` int DEFAULT '0',
  `tlr_present_2` int DEFAULT '0',
  `tlr_present_3` int DEFAULT '0',
  `clk_sd_auth` int DEFAULT '0',
  `clk_sd_hs` int DEFAULT '0',
  `clk_sd_held` int DEFAULT '0',
  `clk_sd_av` int DEFAULT '0',
  `clk_sd_dist_hq` int DEFAULT '0',
  `clk_sd_dist_1` int DEFAULT '0',
  `clk_sd_dist_2` int DEFAULT '0',
  `clk_sd_dist_3` int DEFAULT '0',
  `clk_sd_state_hq` int DEFAULT '0',
  `clk_sd_state_1` int DEFAULT '0',
  `clk_sd_state_2` int DEFAULT '0',
  `clk_sd_state_3` int DEFAULT '0',
  `clk_sd_present_hq` int DEFAULT '0',
  `clk_sd_present_1` int DEFAULT '0',
  `clk_sd_present_2` int DEFAULT '0',
  `clk_sd_present_3` int DEFAULT '0',
  `ere_auth` int DEFAULT '0',
  `ere_hs` int DEFAULT '0',
  `ere_held` int DEFAULT '0',
  `ere_av` int DEFAULT '0',
  `ere_dist_hq` int DEFAULT '0',
  `ere_dist_1` int DEFAULT '0',
  `ere_dist_2` int DEFAULT '0',
  `ere_dist_3` int DEFAULT '0',
  `ere_state_hq` int DEFAULT '0',
  `ere_state_1` int DEFAULT '0',
  `ere_state_2` int DEFAULT '0',
  `ere_state_3` int DEFAULT '0',
  `ere_present_hq` int DEFAULT '0',
  `ere_present_1` int DEFAULT '0',
  `ere_present_2` int DEFAULT '0',
  `ere_present_3` int DEFAULT '0',
  `total_auth` int DEFAULT '0',
  `total_hs` int DEFAULT '0',
  `total_held` int DEFAULT '0',
  `total_av` int DEFAULT '0',
  `total_dist_hq` int DEFAULT '0',
  `total_dist_1` int DEFAULT '0',
  `total_dist_2` int DEFAULT '0',
  `total_dist_3` int DEFAULT '0',
  `total_state_hq` int DEFAULT '0',
  `total_state_1` int DEFAULT '0',
  `total_state_2` int DEFAULT '0',
  `total_state_3` int DEFAULT '0',
  `total_present_hq` int DEFAULT '0',
  `total_present_1` int DEFAULT '0',
  `total_present_2` int DEFAULT '0',
  `total_present_3` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `report_date` (`report_date`),
  KEY `idx_report_date` (`report_date`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_manpower_daily`
--

LOCK TABLES `trade_manpower_daily` WRITE;
/*!40000 ALTER TABLE `trade_manpower_daily` DISABLE KEYS */;
/*!40000 ALTER TABLE `trade_manpower_daily` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `units_served`
--

DROP TABLE IF EXISTS `units_served`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `units_served` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `unit` varchar(255) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `duty_performed` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_units` (`personnel_id`),
  CONSTRAINT `units_served_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=186 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units_served`
--

LOCK TABLES `units_served` WRITE;
/*!40000 ALTER TABLE `units_served` DISABLE KEYS */;
INSERT INTO `units_served` VALUES (98,66,'15689681K',1,'2 MDSR','2005-10-01','2008-03-10','SYSTEM'),(99,66,'15689681K',2,'29 IDSR','2008-03-11','2010-10-21',''),(100,66,'15689681K',3,'20 RR BN','2010-10-21','2011-09-25',''),(101,66,'15689681K',4,'CENTRAL COMDT SIG REGT','2011-09-25','2014-07-06',''),(102,66,'15689681K',5,'16 (I) ABSL','2014-07-06','2017-03-31',''),(103,66,'15689681K',6,'56 INF DIV SIG REGT','2017-10-22','2019-10-22',''),(109,68,'15728668I',1,'21 MDSR','2012-03-12','2014-04-10',''),(110,68,'15728668I',2,'39 MDSR','2014-04-12','2016-05-15',''),(119,64,'15719460P',1,'33 ADSR','2011-10-15','2013-08-02','RADIO'),(120,64,'15719460P',2,'HQ CIF (D) FORCE SIG REGT','2013-08-02','2015-12-15','SIG CEN'),(121,64,'15719460P',3,'5 CSR','2015-12-15','2018-08-06','BSNL'),(122,64,'15719460P',4,'10 RAPID SIG REGT','2018-08-06','2021-06-30','EXCHANGE'),(123,64,'15719460P',5,'4 IDSR','2021-06-30','2023-11-18','EXCHANGE'),(133,40,'15720341L',1,'41 NSR','2012-01-01','2015-01-01',''),(134,40,'15720341L',2,'25 IDSR','2015-01-02','2017-01-02',''),(135,40,'15720341L',3,'54 IDSR','2017-01-03','2020-01-03',''),(136,40,'15720341L',4,'24 IDSR','2020-01-03','2023-01-03',''),(144,42,'15736949K',1,'31 ADSR','2016-04-03','2019-05-15',''),(145,42,'15736949K',2,'33 ADSR','2019-06-15','2023-01-13',''),(149,56,'A4351981P',1,'22 RSR','2023-09-02','2025-08-25',''),(150,57,'15740527W',1,'16 IDSR','2017-01-10','2019-10-09',''),(151,57,'15740527W',2,'17 CSR','2019-10-10','2022-08-22',''),(152,57,'15740527W',3,'31 NSR','2022-08-23','2025-09-30',''),(153,60,'15731634W',1,'71 IDSR','2013-11-20','2015-12-25',''),(154,60,'15731634W',2,'21 SIGNAL GP','2015-12-25','2019-05-07',''),(155,60,'15731634W',3,'1RR BN','2019-05-07','2022-10-05',''),(156,60,'15731634W',4,'33 ADSR','2022-10-05','2025-10-07',''),(157,72,'15734096Y',1,'NCSR','2014-11-21','2017-05-31','EXCHANGE'),(158,72,'15734096Y',2,'UNIT 832','2017-05-31','2021-04-06',''),(159,72,'15734096Y',3,'31 ADSR','2021-04-07','2023-12-19',''),(160,41,'15743230A',1,'54IDSR','2023-12-06','2025-09-23','NFS'),(161,50,'A4203413X',1,'PQTS','2026-02-10','2026-02-10','RR'),(162,131,'15744564F',1,'19 IDSR','2018-04-15','2020-09-29','SYSTEM'),(164,86,'15718811M',1,'9IDSR(A)','2021-07-15','2024-01-14','STOREMAN'),(168,133,'12345t',1,'RED','2022-01-13','2025-06-13',''),(169,135,'12345EE',1,'RED','2022-01-13','2025-06-13',''),(175,132,'15734024P',1,'57 WEU','2023-06-13','2025-12-31','CHM'),(181,67,'15716045H',1,'2MDSR','2011-03-30','2014-03-11','TM'),(182,67,'15716045H',2,'12 WEU','2014-04-17','2016-12-16','SYSTEM'),(183,67,'15716045H',3,'20 MDSR','2016-12-16','2018-10-26','EXCHANGE'),(184,67,'15716045H',4,'57 RR','2018-10-26','2021-09-10','RUNNER'),(185,67,'15716045H',5,'WCSR','2021-09-10','2024-05-21','CHM');
/*!40000 ALTER TABLE `units_served` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_messages`
--

DROP TABLE IF EXISTS `user_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message` text,
  `sent_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `is_read` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  CONSTRAINT `user_messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_messages`
--

LOCK TABLES `user_messages` WRITE;
/*!40000 ALTER TABLE `user_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `company` varchar(50) DEFAULT '1 company',
  `army_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'COL M S DILAWRI','co','123','CO','2025-11-19 06:28:38','Admin',NULL),(2,'MAJ PRATEEK','oc1','123','OC','2025-11-19 06:42:10','1 company',NULL),(3,'ANUJ','adjt','123','ADJUTANT','2025-11-19 06:45:22','Admin',NULL),(4,'MANOJ SINGH','manoj.jco@gmail.com','123','JCO','2025-11-18 04:52:55','1 company',NULL),(5,'AKHILESH VERMA','akhil.jco@gmail.com','123','JCO','2025-11-18 06:15:33','1 company',NULL),(11,'P RASTOGI','oc2','123','OC','2025-12-16 01:40:20','2 Company',NULL),(19,'MAJ VISHAL DIXIT','2ic','123','2IC','2025-12-31 06:48:12','Admin',NULL),(20,'S S RAO','ocennco','123','O CENTRE NCO','2026-01-10 06:00:29','Center','15712365w'),(21,'Subedar_Ram','subedar.ram@army.local','123','JCO','2026-01-14 05:50:39','1 company','984CESR'),(22,'Subedar_Mohan','subedar.mohan@army.local','123','JCO','2026-01-14 05:50:39','2 company',NULL),(23,'NaibSubedar_Singh','naib.singh@army.local','123','JCO','2026-01-14 05:50:39','3 company',NULL),(24,'NaibSubedar_Kumar','naib.kumar@army.local','123','JCO','2026-01-14 05:50:39','HQ company','99999CESR'),(25,'ANOOP J S','1coyonco','123','ONCO','2026-01-12 07:27:53','1 company',NULL),(26,'SANJAY DAS','2coyonco','123','ONCO','2026-01-12 07:27:53','2 company',NULL),(27,'ROHIT KUMAR','3coyonco','123','ONCO','2026-01-12 07:27:53','3 company',NULL),(28,'PAWAN SHARMA','hqcoyonco','123','ONCO','2026-01-12 07:27:53','HQ company',NULL),(29,'R K TOMAR','trgjco','123','TRGJCO','2026-01-16 06:20:50','HQ company',NULL),(30,'john.doe','acctoffr','123','ACCOUNT OFFICER','2026-01-19 08:43:14','HQ company','ARMY12345'),(31,'smith.doe','projoffr','123','PROJECT OFFICER','2026-01-19 08:47:14','HQ company','ARMY1254345'),(32,'naidu','projjco','123','PROJECT JCO','2026-01-19 19:52:57','HQ company','123456099'),(33,'G G','sm','123','Subedar Major','2026-01-19 20:21:49','HQ company',NULL),(34,'Prakash ','acctjco','123','ACCOUNT JCO','2026-01-19 20:49:44','HQ company','98965565'),(35,'kesti','kesti@123','123','JCO','2026-01-19 23:12:05','1 company','775CESR'),(36,'SATENDRA KUMAR','sjcohq','123','S/JCO','2026-01-20 00:00:56','HQ company','A43673A'),(37,'MOHAN LAL','sjco1','123','S/JCO','2026-01-20 02:12:21','1 company','JC457693'),(38,'Hansram ','ram@123','123','JCO','2026-01-20 02:12:21','1 company','jc393919L'),(39,'nco_pwr_c1','ncopwr','123','NCO PWR','2026-01-21 06:08:12','1 company','C1-1001'),(40,'nco_chq_c1','ncochq1','123','NCO CHQ','2026-01-21 06:08:12','1 company','C1-1002'),(41,'GHANSHYAM MAHLA','ncoit','123','NCO IT','2026-01-21 06:08:12','1 company','15718811M'),(42,'JITENDRA SINGH','ncomw','123','NCO MW','2026-01-21 06:08:12','1 company','15730189W'),(43,'nco_line_c1','ncoline','123','NCO LINE','2026-01-21 06:08:12','1 company','C1-1005'),(44,'nco_op_c1','ncoop','123','NCO OP','2026-01-21 06:08:12','1 company','C1-1006'),(45,'nco_mccs_c2','ncomccs','123','NCO MCCS','2026-01-21 06:09:34','2 company','C2-2001'),(46,'nco_chq_c2','ncochq2','123','NCO CHQ','2026-01-21 06:09:34','2 company','C2-2002'),(47,'nco_rhq_c3','ncorhq','123','NCO RHQ','2026-01-21 06:10:42','HQ company','C3-3001'),(48,'nco_chq_c3','ncochqhq','123','NCO CHQ','2026-01-21 06:10:42','HQ company','C3-3002'),(49,'nco_lrw_c3','ncolrw','123','NCO LRW','2026-01-21 06:10:42','HQ company','C3-3003'),(50,'nco_qm_c3','ncoqm','123','NCO QM','2026-01-21 06:10:42','HQ company','C3-3004'),(51,'nco_mt_c3','ncomt','123','NCO MT','2026-01-21 06:10:42','HQ company','C3-3005'),(52,'nco_tm_c3','ncotm','123','NCO TM','2026-01-21 06:10:42','HQ company','C3-3006'),(53,'nco_rp_c3','ncorp','123','NCO RP','2026-01-21 06:10:42','HQ company','C3-3007'),(56,'jco_pwr_1','jcopwr','123','JCO PWR','2026-01-21 07:12:15','1 company','JCO-1001'),(57,'jco_chq_1','jcochq1','123','JCO CHQ','2026-01-21 07:12:15','1 company','JCO-1002'),(58,'jco_it_1','jcoit','123','JCO IT','2026-01-21 07:12:15','1 company','JCO-1003'),(59,'jco_mw_1','jcomw','123','JCO MW','2026-01-21 07:12:15','1 company','JCO-1004'),(60,'jco_line_1','jcoline','123','JCO LINE','2026-01-21 07:12:15','1 company','JCO-1005'),(61,'jco_op_1','jcoop','123','JCO OP','2026-01-21 07:12:15','1 company','JCO-1006'),(62,'jco_mccs_2','jcomccs','123','JCO MCCS','2026-01-21 07:41:45','2 company','JCO-1007'),(63,'jco_chq_2','jcochq2','123','JCO CHQ','2026-01-21 07:41:45','2 company','JCO-1008'),(64,'jco_chq_hq','jcochqhq','123','JCO CHQ','2026-01-21 07:41:45','HQ company','JCO-1009'),(65,'jco_rhq_hq','jcorhq','123','JCO RHQ','2026-01-21 07:41:45','HQ company','JCO-1010'),(66,'jco_tm_hq','jcotm','123','JCO TM','2026-01-21 07:41:45','HQ company','JCO-1011'),(67,'jco_mt_hq','jcomt','123','JCO MT','2026-01-21 07:41:45','HQ company','JCO-1012'),(69,'jco_lrw_hq','jcolrw','123','JCO LRW','2026-01-21 07:41:45','HQ company','JCO-1013'),(70,'jco_rp_hq','jcorp','123','JA','2026-01-21 07:41:45','HQ company','JCO-1014'),(71,'jco_qm_hq','jcoqm','123','JCO QM','2026-01-21 07:41:45','HQ company','JCO-1015'),(72,'SUB MUKESH KUMAR','headclk','123','HEAD CLK','2026-02-09 03:35:12','Center','JCO-1016'),(73,'ANKIT KUMAR','PA','123','PA','2026-02-09 03:35:53','Center','15756452P'),(74,'CAPT S SENAPATI','ochq','123','OC','2026-02-09 03:36:54','HQ company',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_detail`
--

DROP TABLE IF EXISTS `vehicle_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_detail` (
  `vehicle_no` varchar(20) NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  `detailment` varchar(100) DEFAULT NULL,
  `dist_travelled` int DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `bullet_proof` enum('Y','N') DEFAULT NULL,
  PRIMARY KEY (`vehicle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_detail`
--

LOCK TABLES `vehicle_detail` WRITE;
/*!40000 ALTER TABLE `vehicle_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicle_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_info`
--

DROP TABLE IF EXISTS `weight_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight_info` (
  `troop_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `army_number` varchar(50) DEFAULT NULL,
  `actual_weight` float DEFAULT NULL,
  `age` int DEFAULT NULL,
  `height` float DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `status_type` varchar(10) NOT NULL DEFAULT 'safe',
  `category_type` varchar(10) DEFAULT NULL,
  `restrictions` text,
  PRIMARY KEY (`troop_id`),
  UNIQUE KEY `army_number` (`army_number`),
  UNIQUE KEY `army_number_2` (`army_number`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_info`
--

LOCK TABLES `weight_info` WRITE;
/*!40000 ALTER TABLE `weight_info` DISABLE KEYS */;
INSERT INTO `weight_info` VALUES (33,'SR PANDEY','HAV','15689681K',82,41,183,'1 Company','shape',NULL,NULL),(38,'PRADEEP BABU','NK','15717264F',70,36,170,'1 Company','shape',NULL,NULL),(39,'ADARASH KUMAR SABU','Agniveer','A4200038M',63,22,170,'1 Company','shape',NULL,NULL),(40,'LAXMAN MUNDA','NK','15724953A',72,37,170,'1 Company','shape',NULL,NULL),(41,'SUNIL KUMAR','NK','15720596L',75,37,173,'1 Company','shape',NULL,NULL),(42,'RAVI','Agniveer','A4204797K',60,22,174,'1 Company','shape',NULL,NULL),(43,'RAM SINGH','HAV','15688598A',NULL,44,17,'1 Company','shape',NULL,NULL),(44,'RAJESH CHAURASIA','HAV','15716216K',72,38,177,'1 Company','shape',NULL,NULL),(45,'SUNIL KUMAR YADAV','NK','15709802K',64,38,172,'1 Company','shape',NULL,NULL),(47,'PREM MOHAN','HAV','15719951L',79,36,186,'1 Company','shape',NULL,NULL),(49,'JINCE L','HAV','15731820M',75,31,177,'1 Company','shape',NULL,NULL),(50,'JEBIN PAUL K','NK','15740143F',90,30,182,'1 Company','shape',NULL,NULL),(51,'MD SUJAN MIRZA','NK','15749660A',83,28,182,'1 Company','shape',NULL,NULL),(52,'MOHANRAJ T','NK','15753860N',76,30,180,'1 Company','shape',NULL,NULL),(53,'ASWIN M','Agniveer','A4201316F',65,24,172,'1 Company','shape',NULL,NULL),(55,'GAIKWAD RAHUL SUNIL','Agniveer','A4204643X',59,23,171,'1 Company','shape',NULL,NULL),(56,'VIVEK KUMAR SRIVASTAV','Agniveer','A4352497P',63,22,174,'1 Company','shape',NULL,NULL),(57,'ROSHAN KESHARWANI','Agniveer','A4203079F',65,24,170,'1 Company','shape',NULL,NULL),(58,'GIDIJALA VENNKATA RAMANA ','Agniveer','A4351064L',59,23,171,'1 Company','shape',NULL,NULL),(59,'EROTHU RAKESH','Agniveer','A4351041K',61,25,169,'1 Company','shape',NULL,NULL),(60,'SHAILENDRA SINGH','NK','1574165Y',74,31,178,'1 Company','shape',NULL,'AS PER MED BD'),(61,'PANDURANG B K','HAV','15692903Y',70,42,170,'1 Company','shape',NULL,NULL),(62,'AMIT RANJAN','HAV','15720931K',74,37,174,'1 Company','shape',NULL,NULL),(63,'T. RAMESH BABU','HAV','15681641N',76,43,174,'1 Company','shape',NULL,NULL),(67,'ADARSH S','HAV','15719460P',84,33,174,'1 Company','shape',NULL,NULL),(68,'DURGESH KHAROLE','L HAV','15722524A',85,34,174,'1 Company','shape',NULL,NULL),(69,'RAVI KANT','LOC NK','15724706M',81,36,176,'1 Company','shape',NULL,NULL),(70,'PRADEEP KUMAR NAHAK','Agniveer','A4203499F',68,22,182,'1 Company','shape',NULL,NULL),(71,'VIJAY PAL','Agniveer','A4204720F',63,22,168,'1 Company','shape',NULL,NULL),(73,'MANOHAR KUMAR','L HAV','15732973H',75,33,174,'1 Company','shape',NULL,NULL),(74,'AMBRESH','Agniveer','A4205053L',51,21,167,'1 Company','shape',NULL,NULL),(75,'SUDISH KUMAR','L NK','15748339K',64,30,172,'1 Company','shape',NULL,NULL),(76,'SUKHDEV','L NK','15736649H',85,30,172,'1 Company','shape',NULL,NULL),(77,'PADIGELA RAMESH','NK','15721376N',75,33,175,'1 Company','shape',NULL,NULL),(78,'UPPARA MADHU','Agniveer','A4204683Y',59,20,167,'1 Company','shape',NULL,NULL),(79,'ANIL CHALAWADI','Agniveer','A4204856L',57,22,168,'1 Company','shape',NULL,NULL),(80,'AMAN KUMAR','Agniveer','A4203556X',70,23,172,'1 Company','shape',NULL,NULL),(81,'HEMANTA DEY','Agniveer','A4205008Y',63,23,180,'1 Company','shape',NULL,NULL),(82,'PAWAR SANKET SANJAY','Agniveer','A4204930F',62,23,172,'1 Company','shape',NULL,NULL),(85,'ASHISH KUMAR GUPTA','Agniveer','A4205213A',65,20,172,'1 Company','shape',NULL,NULL),(86,'SAJAN','Agniveer','A4200365X',64,21,174,'1 Company','shape',NULL,NULL),(89,'SHUBHAM','Agniveer','A4205888A',58,20,174,'1 Company','shape',NULL,NULL),(90,'RAUT PANKAJ J','L NK','15749159N',76,29,170,'1 Company','shape',NULL,NULL),(91,'HARIBALA S','Agniveer','A4206051M',54,22,170,'1 Company','shape',NULL,NULL),(95,'SENTHIL KUMAR G','NK','15720341L',85,36,180,'1 Company','shape',NULL,NULL),(99,'MOHAN KUMAR YADAV','NK','15736949K',77,33,172,'1 Company','shape',NULL,NULL),(100,'DHANANJAY KUMAR YADAV','NK','15740970K',74,32,169,'1 Company','shape',NULL,NULL),(103,'UDAY KUMAR','Agniveer','A4203816X',68,22,170,'1 Company','shape',NULL,NULL),(107,'RAJPUT VIKAS','Agniveer','A4351981P',59,23,168,'1 Company','shape',NULL,NULL),(109,'ABHISHEK YADAV','Agniveer','A4207474M',52,22,163,'1 Company','shape',NULL,NULL),(110,'G SREENIVASULU','HAV','15715916L',74,35,180,'1 Company','shape',NULL,NULL),(111,'SATYENDRA SINGH','L NK','15742217K',82,29,173,'1 Company','shape',NULL,NULL),(112,'SUDHIR KUMAR','Signal Man','15756017Y',86,26,175,'1 Company','shape',NULL,NULL),(113,'RAHUL LAGAD D','Agniveer','A4205388H',56,21,168,'1 Company','shape',NULL,NULL),(114,'ABHISHEK KUMAR YADAV','Signal Man','15752536K',65.5,28,168,'1 Company','shape',NULL,NULL),(115,'SWAPANIR KUMAR','Signal Man','15706852K',71,39,173,'1 Company','shape',NULL,NULL),(116,'ANKIT SINGH TOMAR','Agniveer','A4204811L',67,22,173,'1 Company','shape',NULL,NULL),(117,'Majgaonkar Rushikesh Prakash','Agniveer','A4203007X',65,24,170,'1 Company','shape',NULL,NULL),(118,'BRAJESH TIWARI','NK','15740527W',69,34,172,'1 Company','shape',NULL,NULL),(119,'ARVIND GUPTA','NK','15740824K',73,31,170,'1 Company','shape',NULL,NULL),(120,'BRIJESH KUMAR TIWARI','NK','15731634W',66,31,171,'1 Company','shape',NULL,NULL),(121,'SHAHIL','Agniveer','A4353823Y',70,22,176,'1 Company','shape',NULL,NULL),(122,'BATTINI RANGASWAMY','NK','15734096Y',68,32,169,'1 Company','shape',NULL,NULL),(123,'PATIL AKASJ RAJARAM','Agniveer','A4354515L',60,23,176,'1 Company','shape',NULL,NULL),(124,'MANE PRAIWAL K','Agniveer','A4354369W',62,22,169,'1 Company','shape',NULL,NULL),(125,'ASHISH SINGH','Agniveer','A4350867L',67,21,176,'1 Company','shape',NULL,NULL),(126,'Hansram ','Naib Subedar','jc393919L',72,33,176,'1 Company','shape',NULL,NULL),(128,'JITENDRA SINGH','NK','15730189W',76,32,178,'1 Company','shape',NULL,NULL),(131,'GIRI AJINATH BABAN','L NK','15743230A',67,29,168,'1 Company','shape',NULL,NULL),(135,'SUNIL GODARA','Agniveer','A4203413X',62.5,21,179,'1 Company','shape',NULL,NULL),(136,'AMRENDRA SHUKLA ','L NK','15744564F',80,31,185,'HQ company','shape',NULL,NULL),(138,'GHANSHYAM MAHLA','HAV','15718811M',78,34,182,'1 Company','shape',NULL,NULL),(143,'CODERWW','Agniveer','12345EE',78,25,178,'1 Company','shape',NULL,NULL),(147,'PUSHPENDRA','HAV','15734024P',79,34,178,'1 Company','shape',NULL,NULL),(149,'S K GUPTA','NK','15716045H',73,39,170,'1 Company','shape',NULL,NULL);
/*!40000 ALTER TABLE `weight_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-18 16:04:29
