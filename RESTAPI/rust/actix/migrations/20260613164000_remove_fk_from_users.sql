-- Migration: remove_fk_from_users
-- Remove FK constraint from users.clinic_id so cloud-synced accounts
-- can reference clinics that don't exist in the local database.

PRAGMA foreign_keys = OFF;

CREATE TABLE IF NOT EXISTS users_new (
    id TEXT PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    role VARCHAR(200) NOT NULL,
    status VARCHAR(100) NOT NULL,
    clinic_id TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    updated_at TEXT
);

INSERT INTO users_new SELECT * FROM users;
DROP TABLE users;
ALTER TABLE users_new RENAME TO users;

CREATE INDEX IF NOT EXISTS idx_users_clinic_id ON users(clinic_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);

PRAGMA foreign_keys = ON;
