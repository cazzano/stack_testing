-- Migration: added_password_hash
-- Created at: 2026-06-13 21:53:52


-- Drop table: tbl
DROP TABLE IF EXISTS tbl;
-- Add column: users.password
ALTER TABLE users ADD COLUMN password STRING NOT NULL DEFAULT '';
-- Change column type: tokens.revoke
ALTER TABLE tokens DROP COLUMN revoke;
ALTER TABLE tokens ADD COLUMN revoke INTEGER NOT NULL DEFAULT 0;
