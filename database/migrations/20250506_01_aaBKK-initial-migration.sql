-- initial migration
-- depends: 

CREATE SCHEMA IF NOT EXISTS financial;

CREATE TABLE financial.entity (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    status BOOLEAN NOT NULL
);

CREATE TABLE financial.acc_payable (
    id SERIAL PRIMARY KEY,
    id_entity INTEGER NOT NULL,
    type VARCHAR(30) NOT NULL,
    cost DECIMAL(11,3) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    status BOOLEAN NOT NULL DEFAULT true,
    compost_id VARCHAR(30) UNIQUE GENERATED ALWAYS AS (id_entity::varchar || '-' || "type" || '-' || cost::varchar) STORED,
    FOREIGN KEY (id_entity) REFERENCES financial.entity(id)
);
