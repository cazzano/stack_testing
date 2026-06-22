-- Migration: move_gender_from_prescription_to_patients
-- Created at: 2026-06-16 01:07:40

ALTER TABLE patients ADD COLUMN gender VARCHAR(100);
ALTER TABLE prescription DROP COLUMN gender;
