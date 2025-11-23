-- Script para crear la base de datos y la tabla de contactos en MySQL

CREATE DATABASE IF NOT EXISTS cloudcontacts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cloudcontacts;

CREATE TABLE IF NOT EXISTS contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_logico TINYINT(1) NOT NULL DEFAULT 0
);
