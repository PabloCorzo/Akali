CREATE DATABASE IF NOT EXISTS films CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE films;

CREATE TABLE IF NOT EXISTS peliculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title    VARCHAR(200) NOT NULL,
    director VARCHAR(200),
    actors   TEXT,
    synopsis TEXT
);
