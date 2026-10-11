CREATE DATABASE IF NOT EXISTS farmer_market_db;
USE farmer_market_db;

CREATE TABLE IF NOT EXISTS farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS market_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    market_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_market_price (crop, location, market_name)
);

CREATE TABLE IF NOT EXISTS farmer_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    crop VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_farmer_crop_location (farmer_id, crop, location),
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE
);

INSERT IGNORE INTO farmers (username, password) VALUES ('farmer1','1234');
INSERT IGNORE INTO admins (username, password) VALUES ('admin1','admin123');

INSERT IGNORE INTO market_prices (crop,location,market_name,price) VALUES
('Tomato','Hyderabad','Bowenpally Market',30),
('Tomato','Hyderabad','Gudimalkapur Market',34),
('Tomato','Hyderabad','Rythu Bazaar',38),
('Tomato','Warangal','Warangal Market',36),
('Tomato','Warangal','Enumamula Market',41),
('Rice','Hyderabad','Rythu Bazaar',42),
('Rice','Hyderabad','Bowenpally Market',45),
('Rice','Warangal','Warangal Market',48);
