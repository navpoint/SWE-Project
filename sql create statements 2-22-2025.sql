

CREATE DATABASE finance_tracker;

CREATE TABLE `cash_flows` (
   `flow_id` int NOT NULL AUTO_INCREMENT,
   `user_id` int NOT NULL,
   `amount` decimal(10,2) NOT NULL,
   `category` varchar(100) DEFAULT NULL,
   `description` text,
   `flow_type` enum('income','expense') NOT NULL,
   `frequency` enum('One Time','Daily','Weekly','Monthly','Quarterly','Annually') NOT NULL,
   `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`flow_id`),
   KEY `user_id` (`user_id`),
   CONSTRAINT `cash_flows_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
 );
 
 CREATE TABLE `events` (
   `event_id` int NOT NULL AUTO_INCREMENT,
   `user_id` int NOT NULL,
   `goal_id` int NOT NULL,
   `description` text NOT NULL,
   `event_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`event_id`),
   KEY `user_id` (`user_id`),
   KEY `events_ibfk_2` (`goal_id`),
   CONSTRAINT `events_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
   CONSTRAINT `events_ibfk_2` FOREIGN KEY (`goal_id`) REFERENCES `goals` (`goal_id`) ON DELETE CASCADE
 );
 
 CREATE TABLE `goals` (
   `goal_id` int NOT NULL AUTO_INCREMENT,
   `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   `user_id` int NOT NULL,
   `name` varchar(100) NOT NULL,
   `description` text,
   `target_amount` decimal(10,2) DEFAULT NULL,
   `progress` decimal(10,2) DEFAULT '0.00',
   `is_current` char(1) NOT NULL DEFAULT 'Y',
   `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`goal_id`),
   UNIQUE KEY `goal_id` (`goal_id`,`modified_at`),
   KEY `user_id` (`user_id`),
   CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
 ); 
 
 CREATE TABLE `plans` (
   `plan_id` int NOT NULL AUTO_INCREMENT,
   `user_id` int NOT NULL,
   `name` varchar(100) NOT NULL,
   `description` text,
   `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`plan_id`),
   KEY `user_id` (`user_id`),
   CONSTRAINT `plans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
 ) ;
 
 CREATE TABLE `users` (
   `user_id` int NOT NULL AUTO_INCREMENT,
   `first_name` varchar(50) NOT NULL,
   `last_name` varchar(50) DEFAULT NULL,
   `username` varchar(50) NOT NULL,
   `email` varchar(100) NOT NULL,
   `password_hash` varchar(255) NOT NULL,
   `date_of_birth` date NOT NULL,
   `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`user_id`),
   UNIQUE KEY `username` (`username`),
   UNIQUE KEY `email` (`email`)
 ) 