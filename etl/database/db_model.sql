/* 
Elegí Postgres como motor de base de datos por su facilidad de uso y por ser open source.
Además, me pareció personalmente que el ejercicio se prestaba a usar un motor de base de datos relacional.
*/

-- No usamos create ni use puesto que  la bd es creada al momento del arranque del contenedor de docker.

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
    updated_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

