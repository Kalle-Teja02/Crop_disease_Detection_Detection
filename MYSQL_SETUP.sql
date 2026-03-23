-- ============================================================================
-- Crop Disease Detection - MySQL Database Setup
-- ============================================================================
-- This script creates the MySQL database and tables for the crop disease
-- detection system. Run this script on your MySQL server before deploying.
-- ============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS crop_disease_db;
USE crop_disease_db;

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_path VARCHAR(255) NOT NULL,
    disease VARCHAR(100) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_disease (disease),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Optional: Create user for the application (recommended for security)
-- ============================================================================
-- Uncomment and modify the following lines to create a dedicated MySQL user:
-- 
-- CREATE USER 'crop_disease_user'@'localhost' IDENTIFIED BY 'your_secure_password';
-- GRANT ALL PRIVILEGES ON crop_disease_db.* TO 'crop_disease_user'@'localhost';
-- FLUSH PRIVILEGES;
--
-- Then update your app.py MYSQL_CONFIG with:
-- MYSQL_CONFIG = {
--     'host': 'localhost',
--     'user': 'crop_disease_user',
--     'password': 'your_secure_password',
--     'database': 'crop_disease_db'
-- }

-- ============================================================================
-- Verify setup
-- ============================================================================
-- Run these commands to verify the setup:
-- SELECT * FROM crop_disease_db.predictions;
-- SHOW TABLES IN crop_disease_db;
-- DESCRIBE crop_disease_db.predictions;
