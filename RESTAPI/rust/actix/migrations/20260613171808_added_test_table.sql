-- Migration: added_test_table
-- Created at: 2026-06-13 17:18:08


-- Create table: tbl
CREATE TABLE IF NOT EXISTS tbl (

	id TEXT PRIMARY KEY,
	lol TEXT
);
-- Change column type: tokens.revoke
ALTER TABLE tokens DROP COLUMN revoke;
ALTER TABLE tokens ADD COLUMN revoke INTEGER NOT NULL DEFAULT 0;
