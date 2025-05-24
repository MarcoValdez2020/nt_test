/* 
Elegí Postgres como motor de base de datos por su facilidad de uso y por ser open source.
Además, me pareció personalmente que el ejercicio se prestaba a usar un motor de base de datos relacional.
*/

-- No usamos create ni use puesto que  la bd es creada al momento del arranque del contenedor de docker.

-- Creación de la tabla de companies
CREATE TABLE IF NOT EXISTS companies (
    company_id CHAR(40) PRIMARY KEY NOT NULL,
    company_name VARCHAR(130) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

/* Creacion de un ENUM para el status de los charges con los valores obtenidos a partir de revisar la data manualmente
    - voided
    - pending_payment
    - paid
    - pre_authorized
    - refunded
    - charged_back
    - expired
    - partially_refunded
*/
CREATE TYPE charge_status AS ENUM (
    'voided',
    'pending_payment',
    'paid',
    'pre_authorized',
    'refunded',
    'charged_back',
    'expired',
    'partially_refunded'
);


-- Creción de la tabla charges
CREATE TABLE IF NOT EXISTS charges (
    charge_id CHAR(40) PRIMARY KEY NOT NULL,
    company_id CHAR(40) NOT NULL,
    amount NUMERIC(16, 2) NOT NULL,
    status charge_status NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE,
    paid_at DATE DEFAULT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);


-- Creación de la vista para vizualizar los datos de las empresas y sus cargos
CREATE OR REPLACE VIEW view_daily_company_totals AS
SELECT 
    ch.created_at as fecha,
    co.company_id,
    co.company_name,
    SUM(ch.amount)
FROM charges ch
JOIN companies co ON co.company_id = ch.company_id
GROUP BY fecha, co.company_id, co.company_name
ORDER BY fecha, co.company_name ASC;
