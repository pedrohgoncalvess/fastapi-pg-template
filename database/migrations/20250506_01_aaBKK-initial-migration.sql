-- initial migration
-- depends: 

CREATE SCHEMA IF NOT EXISTS base;

CREATE TABLE "base"."user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    inserted_at TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP
);

CREATE TABLE "base"."refresh" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token UUID NOT NULL UNIQUE,
    used BOOLEAN DEFAULT FALSE,
    inserted_at TIMESTAMP NOT NULL
);