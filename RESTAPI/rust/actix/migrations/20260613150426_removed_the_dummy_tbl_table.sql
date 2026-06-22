-- Migration: removed_the_dummy_tbl_table
-- Created at: 2026-06-13 15:04:26


-- Drop table: tbl
DROP TABLE IF EXISTS tbl;
-- Change column type: tokens.revoke
ALTER TABLE tokens DROP COLUMN revoke;
ALTER TABLE tokens ADD COLUMN revoke INTEGER NOT NULL DEFAULT 0;
