-- initial migration
-- depends: 

CREATE SCHEMA IF NOT EXISTS financial;

CREATE OR REPLACE FUNCTION generate_compost_id(
    id_entity integer,
    "type" varchar,
    cost numeric
) RETURNS VARCHAR AS $$
BEGIN
    RETURN cast(id_entity as varchar) || '-' || "type" || '-' || replace(cast(cost as varchar), ',', '-');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE TABLE financial.entity (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    status BOOLEAN NOT NULL
);

CREATE TABLE financial.acc_payable (
    id INTEGER PRIMARY KEY,
    id_entity INTEGER NOT NULL,
    type VARCHAR(10) NOT NULL,
    cost NUMERIC NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    status BOOLEAN NOT NULL DEFAULT true,
    compost_id VARCHAR(30) GENERATED ALWAYS AS (generate_compost_id(id_entity, type, cost)) STORED UNIQUE,
    FOREIGN KEY (id_entity) REFERENCES financial.entity(id)
);

-- Rollback SQL (equivalent to downgrade function)
-- To use for rollback:
-- DROP TABLE financial.acc_payable;
-- DROP TABLE financial.entity;
-- DROP FUNCTION generate_compost_id;