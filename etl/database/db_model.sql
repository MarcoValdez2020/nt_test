/* 
Elegí Postgres como motor de base de datos por su facilidad de uso y por ser open source.
Además, me pareció personalmente que el ejercicio se prestaba a usar un motor de base de datos relacional.
*/

-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS next_technologies;

-- Conexión a la base de datos
USE next_technologies;

-- Creación de la tabla de companies
CREATE TABLE IF NOT EXISTS companies (
    company_id CHAR(40) PRIMARY KEY NOT NULL,
    company_name VARCHAR(130) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Creción de la tabla charges
CREATE TABLE IF NOT EXISTS charges (
    charge_id CHAR(40) PRIMARY KEY NOT NULL,
    company_id CHAR(40) NOT NULL,
    charge_name VARCHAR(130) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

