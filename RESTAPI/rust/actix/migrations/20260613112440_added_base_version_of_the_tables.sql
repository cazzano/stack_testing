-- Migration: added_base_version_of_the_tables
-- Created at: 2026-06-13 11:24:40


-- Create table: clinics
CREATE TABLE IF NOT EXISTS clinics (
    id TEXT PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    updated_at TEXT
);
-- Create table: users
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    role VARCHAR(200) NOT NULL,
    status VARCHAR(100) NOT NULL,
    clinic_id TEXT REFERENCES clinics(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_users_clinic_id ON users(clinic_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
-- Create table: tokens
CREATE TABLE IF NOT EXISTS tokens (
    id TEXT PRIMARY KEY,
    token TEXT NOT NULL,
    revoke INTEGER NOT NULL DEFAULT 0,
    user_id TEXT NOT NULL REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_tokens_user_id ON tokens(user_id);
