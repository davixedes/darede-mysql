CREATE DATABASE ecommerce;
USE ecommerce;

CREATE USER dbadmin identified by 'admin';

CREATE TABLE Product (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    description TEXT NULL,
    brand VARCHAR(45) NOT NULL,
    model VARCHAR(100) NOT NULL,
    price DECIMAL(6,2) NOT NULL,
    size DECIMAL(3,2) NOT NULL,
    image LONGBLOB NOT NULL
);

CREATE TABLE Inventory (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    amount INT NOT NULL,
    product_id INT NOT NULL  
);

ALTER TABLE Inventory ADD CONSTRAINT fk_relation_product FOREIGN KEY product_id REFERENCES Product(id);

CREATE TABLE Client (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(70) NOT NULL,
    last_name VARCHAR(70) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE Delivery (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    district VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

ALTER TABLE Delivery ADD CONSTRAINT fk_relation_client FOREIGN KEY address REFERENCES Client(address);

CREATE TABLE Card (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    number INT NOT NULL,
    valid_date DATE NOT NULL,
    holders_name VARCHAR(100) NOT NULL,
    cvv INT NOT NULL
);

ALTER TABLE Card ADD CONSTRAINT fk_relation_client FOREIGN KEY client_id REFERENCES Client(id);

CREATE TABLE Demand (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    disccount DECIMAL(4,2) NULL,
    payment_confirmed BOOLEAN DEFAULT FALSE
);

ALTER TABLE Demand ADD CONSTRAINT fk_relation_card FOREIGN KEY card_id REFERENCES Card(id);
ALTER TABLE Demand ADD CONSTRAINT fk_relation_client FOREIGN KEY card_client_id REFERENCES Card(client_id);
