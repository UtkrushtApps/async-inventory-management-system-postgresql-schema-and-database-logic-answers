-- PostgreSQL schema for Async Inventory Management System

-- Table: categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Table: products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    price NUMERIC(10,2) NOT NULL CHECK(price >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(name, category_id)
);
