CREATE TABLE IF NOT EXISTS clinics (
    id TEXT PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    password STRING NOT NULL,
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

CREATE TABLE IF NOT EXISTS tokens (
    id TEXT PRIMARY KEY,
    token TEXT NOT NULL,
    revoke INTEGER NOT NULL DEFAULT 0,
    user_id TEXT NOT NULL REFERENCES users(id)
);


CREATE INDEX IF NOT EXISTS idx_tokens_user_id ON tokens(user_id);

-- patients
CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    relation VARCHAR(200),
    guardian_name VARCHAR(200),
    phone_number VARCHAR(50),
    email_address VARCHAR(200),
    age INTEGER,
    gender VARCHAR(100),
    cnic INTEGER,
    dob TEXT,
    street_address VARCHAR(500),
    city VARCHAR(200),
    medical_notes TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- visit_records
CREATE TABLE IF NOT EXISTS visit_records (
    id TEXT PRIMARY KEY,
    diagnoses TEXT,
    reason TEXT,
    patient_id TEXT NOT NULL REFERENCES patients(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- medical_history
CREATE TABLE IF NOT EXISTS medical_history (
    id TEXT PRIMARY KEY,
    notes TEXT,
    patient_id TEXT NOT NULL REFERENCES patients(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- billing
CREATE TABLE IF NOT EXISTS billing (
    id TEXT PRIMARY KEY,
    token VARCHAR(200),
    fee REAL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- appointments
CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    status VARCHAR(200),
    type VARCHAR(200),
    reason TEXT,
    patient_id TEXT NOT NULL REFERENCES patients(id),
    patient_name VARCHAR(200),
    doctor_name VARCHAR(200),
    visit_date TEXT,
    preferred_time TEXT,
    doctor_id TEXT REFERENCES users(id),
    billing_id TEXT REFERENCES billing(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- expenses
CREATE TABLE IF NOT EXISTS expenses (
    id TEXT PRIMARY KEY,
    description TEXT,
    category VARCHAR(500),
    amount REAL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- actions
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

-- support_ticket
CREATE TABLE IF NOT EXISTS support_ticket (
    id TEXT PRIMARY KEY,
    full_name VARCHAR(200),
    phone_number VARCHAR(50),
    problem_type VARCHAR(500),
    problem_description TEXT,
    status VARCHAR(200),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- rx_letter
CREATE TABLE IF NOT EXISTS rx_letter (
    id TEXT PRIMARY KEY,
    default_value INTEGER,
    title VARCHAR(200),
    institute_name VARCHAR(500),
    doctor_name VARCHAR(200),
    speciality VARCHAR(500),
    reg_no VARCHAR(500),
    phone VARCHAR(50),
    institute_address TEXT,
    trust_info TEXT,
    logo TEXT,
    vitals INTEGER,
    checklist INTEGER,
    signature INTEGER,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- prescription
CREATE TABLE IF NOT EXISTS prescription (
    id TEXT PRIMARY KEY,
    patient_name VARCHAR(200),
    guardian_name VARCHAR(200),
    age INTEGER,
    phone VARCHAR(50),
    cnic INTEGER,
    doctor_name VARCHAR(200),
    billing_id TEXT REFERENCES billing(id),
    barcode VARCHAR(300),
    diagnoses TEXT,
    clinical_findings TEXT,
    diabetes INTEGER,
    ihd INTEGER,
    hepatitas INTEGER,
    asthma INTEGER,
    pulse VARCHAR(200),
    bp VARCHAR(200),
    respiration VARCHAR(200),
    temperature VARCHAR(200),
    blood_cp INTEGER,
    rbs INTEGER,
    fbs INTEGER,
    viral_marker INTEGER,
    lfts INTEGER,
    rfts INTEGER,
    ecg INTEGER,
    xray INTEGER,
    usg INTEGER,
    advise TEXT,
    rx_letter_id TEXT REFERENCES rx_letter(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- dosage
CREATE TABLE IF NOT EXISTS dosage (
    id TEXT PRIMARY KEY,
    dosage VARCHAR(500),
    frequency VARCHAR(500),
    duration VARCHAR(500),
    prescription_id TEXT NOT NULL REFERENCES prescription(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT,
    deleted_at TEXT
);

-- Indexes for foreign keys
CREATE INDEX IF NOT EXISTS idx_visit_records_patient_id ON visit_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_medical_history_patient_id ON medical_history(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor_id ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_billing_id ON appointments(billing_id);
CREATE INDEX IF NOT EXISTS idx_prescription_rx_letter_id ON prescription(rx_letter_id);
CREATE INDEX IF NOT EXISTS idx_prescription_billing_id ON prescription(billing_id);
CREATE INDEX IF NOT EXISTS idx_dosage_prescription_id ON dosage(prescription_id);
