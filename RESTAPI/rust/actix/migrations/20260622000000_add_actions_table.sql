-- Migration: add_actions_table
-- Created at: 2026-06-22 00:00:00

CREATE TABLE IF NOT EXISTS actions (
    id TEXT PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    domain VARCHAR(200) NOT NULL,
    status VARCHAR(100) NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);
CREATE INDEX IF NOT EXISTS idx_actions_domain ON actions(domain);
