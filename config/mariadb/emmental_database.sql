-- Creates emmental database
CREATE DATABASE IF NOT EXISTS emmental;

-- use 'emmental' db.
use emmental;

CREATE TABLE Users(
	userID CHAR(16) NOT NULL,
	username VARCHAR(30) NOT NULL,
	password VARCHAR(255) NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (userID),
	CONSTRAINT unique_username UNIQUE (username));

CREATE TABLE Content(
	contentID CHAR(16) NOT NULL ,
	userID CHAR(16) NOT NULL,
	filepath VARCHAR(255) NOT NULL,
	creation_date TIMESTAMP NOT NULL,
	CONSTRAINT content_pk PRIMARY KEY (contentID));

CREATE TABLE Logs(
	logID CHAR(16) NOT NULL,
	userID CHAR(16) NOT NULL,
	sessionID CHAR(16) NOT NULL,
	status VARCHAR(30),
	message VARCHAR(255),
	creation_date TIMESTAMP NOT NULL,
	url VARCHAR(255) NOT NULL,
	ip VARCHAR(39) NOT NULL,
	CONSTRAINT logs_pk PRIMARY KEY (logID));

CREATE TABLE Sessions(
	sessionID CHAR(16) NOT NULL,
	userID CHAR(16) NOT NULL,
	expiration TIMESTAMP NOT NULL,
	ip VARCHAR(39) NOT NULL,
	CONSTRAINT session_pk PRIMARY KEY (sessionID));
