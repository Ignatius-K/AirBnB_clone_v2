-- Script prepares the MySQL server for the project
-- Sets up the database and user for test purposes

CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
	IDENTIFIED BY 'hbnb_test_pwd';

CREATE DATABASE IF NOT EXISTS hbnb_test_db;

GRANT ALL PRIVILEGES ON hbnb_test_db.*
	TO 'hbnb_test'@'localhost' WITH GRANT OPTION;

GRANT SELECT ON performance_schema.*
	TO 'hbnb_test_pwd'@'localhost' WITH GRANT OPTION;
