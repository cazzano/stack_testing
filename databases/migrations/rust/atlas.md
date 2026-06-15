# Atlas — Full Guide (The 3 Legendary Steps, Alembic-style)

This is a practical, end-to-end guide to using **Atlas** (atlasgo.io) as the migration tool for the two Rust/actix-web backends (Postgres + SQLite), structured around the same 3-step loop as Alembic:

1. **Edit the schema** (declarative file — your `schema.py` equivalent)
2. **Generate** the migration (`atlas migrate diff`)
3. **Apply** the migration (`atlas migrate apply`)

---

## 1. What Atlas is, in one paragraph

Atlas is a single Go binary (no runtime dependencies) that treats your database schema like Terraform treats infrastructure. You describe the **desired state** of the schema (in plain SQL, Atlas's own HCL DSL, or via an ORM loader), and Atlas computes the diff against either a live database or a migration history, then writes/applies the SQL needed to get there. It supports Postgres, SQLite, MySQL, MariaDB, SQL Server, ClickHouse, CockroachDB, and more — all through the same CLI.

---

## 2. Installation

```bash
# macOS / Linux — official install script
curl -sSf https://atlasgo.sh | sh

# macOS via Homebrew
brew install ariga/tap/atlas

# Docker (no local binary needed)
docker pull arigaio/atlas
docker run --rm arigaio/atlas --help
```

Postgres, SQLite, MySQL, MariaDB, SQL Server, ClickHouse, Redshift, and CockroachDB drivers are bundled in the standard install — no extra steps needed for either of your two backends.

For CI pipelines running inside containers without local Docker access, mount your migrations directory and pass `--net=host`:

```bash
docker run --rm --net=host \
  -v $(pwd)/migrations:/migrations \
  arigaio/atlas migrate apply --url "$DATABASE_URL"
```

---

## 3. Core concepts you need before starting

### 3.1 The "Dev Database"

Several Atlas commands (`migrate diff`, `migrate lint`, `schema apply`) need a **disposable, empty database** to safely simulate schema changes and compute accurate diffs. This is the `--dev-url` flag. Atlas can spin this up for you automatically via Docker:

```bash
--dev-url "docker://postgres/16/dev?search_path=public"   # ephemeral Postgres 16 container
--dev-url "sqlite://file?mode=memory&_fk=1"                # in-memory SQLite
```

Nothing persists in the dev database — it exists only for the duration of the command.

### 3.2 The migration directory and `atlas.sum`

Every `atlas migrate diff` run writes a new timestamped SQL file into your migrations directory (default `file://migrations`), plus updates a checksum file called **`atlas.sum`**:

```
migrations/
├── 20260616120000_initial_schema.sql
├── 20260616121500_add_lock_file_column.sql
└── atlas.sum
```

`atlas.sum` is Atlas's equivalent of guarding against a corrupted/edited migration history — if someone hand-edits an already-applied migration file, `atlas migrate validate` / `atlas migrate lint` will fail with a checksum mismatch. This is stricter than Alembic, which has no built-in integrity check on existing migration files.

### 3.3 Desired state sources

The "desired state" (your `--to` target) can be:
- `file://schema.sql` — plain SQL `CREATE TABLE` statements (closest analog to `schema.py`)
- `file://schema.hcl` — Atlas's Terraform-like DSL
- `file://migrations` — another migration directory (used when diffing two migration histories)
- a live database URL
- an ORM loader (`ent://...`, `atlas-provider-sqlalchemy`, etc. — **no official Rust loader exists**, so for this project we use plain SQL)

---

## 4. Project setup

Recommended layout for the two-backend project:

```
project-root/
├── schema.sql                 # source of truth (Postgres dialect)
├── schema_sqlite.sql          # source of truth (SQLite dialect, if it diverges)
├── atlas.hcl                  # environment config
├── migrations/
│   ├── postgres/
│   │   ├── 20260616120000_initial_schema.sql
│   │   └── atlas.sum
│   └── sqlite/
│       ├── 20260616120000_initial_schema.sql
│       └── atlas.sum
```

### `atlas.hcl`

```hcl
env "postgres" {
  src = "file://schema.sql"
  url = getenv("PG_DATABASE_URL")          // e.g. postgres://user:pass@localhost:5432/app?sslmode=disable
  dev = "docker://postgres/16/dev?search_path=public"

  migration {
    dir = "file://migrations/postgres"
  }
}

env "sqlite" {
  src = "file://schema_sqlite.sql"
  url = getenv("SQLITE_DATABASE_URL")      // e.g. sqlite://app.db?_fk=1
  dev = "sqlite://file?mode=memory&_fk=1"

  migration {
    dir = "file://migrations/sqlite"
  }
}
```

Why two `src` files? Postgres-specific DDL (`gen_random_uuid()`, `UUID` types, generated/computed columns like `clinic_devices.lock_file_hash` from the original Alembic project) has no SQLite equivalent — both Alembic and every Rust tool discussed earlier hit this same wall. Atlas doesn't remove that constraint; it just lets you manage both schema files and both migration histories with one CLI and one config.

If your schema is genuinely identical across both databases (no Postgres-only types/defaults), you can use a single `schema.sql` and just point both envs' `src` at it.

---

## 5. The 3 Legendary Steps — in detail

### Step 1 — Edit the schema file

This is your `schema.py` equivalent. Example — adding `lock_file TEXT` to `clinic_devices`:

```sql
-- schema.sql
CREATE TABLE "clinics" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "name" varchar(200) NOT NULL,
  "city" varchar(200) NULL,
  "phone_number" varchar(100) NULL,
  "email" varchar(100) NULL,
  "status" varchar(90) NULL DEFAULT 'pending',
  "sync" varchar(60) NULL DEFAULT 'not available',
  "created_at" timestamptz NOT NULL DEFAULT now(),
  "updated_at" timestamptz NOT NULL DEFAULT now(),
  "deleted_at" timestamptz NULL,
  PRIMARY KEY ("id")
);

CREATE TABLE "clinic_devices" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "machine_guid" text NULL,
  "computer_name" text NULL,
  "windows_version" text NULL,
  "mac_address" text NULL,
  "status" varchar(300) NULL DEFAULT 'inactive',
  "request_status" varchar(100) NULL DEFAULT 'pending',
  "cpu_serial" text NULL,
  "bios_serial" text NULL,
  "tpm_token" text NULL,
  "lock_file" text NULL,             -- <-- NEW COLUMN ADDED HERE
  "sync" varchar(200) NULL,
  "clinic_id" uuid NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  "updated_at" timestamptz NOT NULL DEFAULT now(),
  "deleted_at" timestamptz NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "clinic_devices_clinic_id_fkey"
    FOREIGN KEY ("clinic_id") REFERENCES "clinics" ("id")
);

-- ... remaining tables (users, clinic_roles, clinic_role_pages, clinic_rules)
```

### Step 2 — Generate the migration

```bash
atlas migrate diff add_lock_file_column \
  --env postgres
```

(With `--env postgres`, the `dir`, `src`, and `dev` values come from `atlas.hcl` automatically — no need to repeat `--dir`/`--to`/`--dev-url` on the command line.)

Atlas will:
1. Spin up the Postgres 16 dev container.
2. Replay every existing migration in `migrations/postgres/` against it, to reconstruct the "current" state.
3. Load `schema.sql` as the "desired" state.
4. Diff the two and write only the delta.

Output:
```
migrations/postgres/20260616121500_add_lock_file_column.sql
```
containing:
```sql
-- Modify "clinic_devices" table
ALTER TABLE "clinic_devices" ADD COLUMN "lock_file" text NULL;
```

`atlas.sum` is updated automatically.

**Without `atlas.hcl`** (equivalent explicit form):
```bash
atlas migrate diff add_lock_file_column \
  --dir "file://migrations/postgres" \
  --to "file://schema.sql" \
  --dev-url "docker://postgres/16/dev?search_path=public"
```

For the SQLite backend, the same command with `--env sqlite`:
```bash
atlas migrate diff add_lock_file_column --env sqlite
```
which under the hood uses `--dev-url "sqlite://file?mode=memory&_fk=1"`.

### Step 3 — Apply the migration

```bash
# Postgres
atlas migrate apply --env postgres

# equivalent explicit form:
atlas migrate apply \
  --dir "file://migrations/postgres" \
  --url "$PG_DATABASE_URL"

# SQLite
atlas migrate apply --env sqlite
# equivalent explicit form:
atlas migrate apply \
  --dir "file://migrations/sqlite" \
  --url "sqlite://app.db?_fk=1"
```

Atlas prints exactly what it's about to run, then applies it and records the new version in its tracking table (`atlas_schema_revisions`) — the equivalent of Alembic's `alembic_version` table.

---

## 6. Side-by-side with Alembic

| | Alembic | Atlas |
|---|---|---|
| Step 1 file | `schema.py` | `schema.sql` (or `schema.hcl`) |
| Step 2 command | `alembic revision --autogenerate -m "msg"` | `atlas migrate diff <name> --env <env>` |
| Step 3 command | `alembic upgrade head` | `atlas migrate apply --env <env>` |
| Rollback one step | `alembic downgrade -1` | `atlas migrate down 1 --env <env>` (Pro feature for some drivers; otherwise via `down.sql` you author or `migrate apply` to an earlier version) |
| Show history | `alembic history` | `atlas migrate status --env <env>` |
| "Is everything in sync?" check | `alembic check` | `atlas migrate lint --env <env> --latest 1` / `atlas schema diff` |
| Integrity of migration files | none built-in | `atlas.sum` + `atlas migrate validate` |
| Version tracking table | `alembic_version` | `atlas_schema_revisions` |
| Per-environment config | `alembic.ini` sections / `env.py` logic | `env "name" { ... }` blocks in `atlas.hcl` |

---

## 7. Extra commands worth knowing

```bash
# Check current applied version vs. available migrations
atlas migrate status --env postgres

# Validate migration directory integrity (checksum) and optionally execute against dev DB
atlas migrate validate --env postgres

# Lint the newest N migrations for destructive/unsafe changes
atlas migrate lint --env postgres --latest 1

# Inspect a live database and dump its schema as SQL or HCL (reverse direction)
atlas schema inspect --url "$PG_DATABASE_URL" --format '{{ sql . }}' > current_schema.sql

# "Terraform apply" style — push schema.sql straight to the DB without a migration file
atlas schema apply --env postgres
```

`atlas migrate lint` is genuinely useful in CI: it flags things like dropping a non-nullable column, adding a `NOT NULL` column without a default to a populated table, renaming columns (which Atlas can detect as drop+add and warn about), and table-locking operations on Postgres.

---

## 8. SQLite-specific notes

- Connection URL format: `sqlite://<path-to-file>?_fk=1` — the `_fk=1` enables SQLite foreign key enforcement, which is off by default and easy to forget.
- Dev database for SQLite is just `sqlite://file?mode=memory&_fk=1` — an in-memory DB, no Docker needed, much faster than spinning up a Postgres container.
- SQLite's `ALTER TABLE` is far more limited than Postgres's (no `DROP COLUMN` before SQLite 3.35, no `ALTER COLUMN TYPE` at all). Atlas handles this by generating the classic SQLite migration pattern under the hood: create a new table with the desired schema, copy data over, drop the old table, rename the new one. This is exactly the kind of thing that's painful to hand-write and where Atlas's autogeneration earns its keep on SQLite specifically.

---

## 9. CI/CD integration

Atlas ships official integrations:
- **GitHub Actions** (`ariga/atlas-action`) — run `atlas migrate lint` on every PR to catch destructive changes before merge, and `atlas migrate apply` on deploy.
- **GitLab CI** templates.
- **Kubernetes Operator** — declare desired schema as a CRD, operator reconciles.
- **Terraform Provider** — manage schema as part of your existing IaC.

A minimal GitHub Actions lint step:
```yaml
- uses: ariga/atlas-action/migrate/lint@v1
  with:
    dir: migrations/postgres
    dir-name: postgres-prod
    dev-url: "docker://postgres/16/dev?search_path=public"
```

Alembic has nothing equivalent built in — you'd write this yourself (e.g., spin up a throwaway DB in CI, run `alembic upgrade head` twice and diff).

---

## 10. Closing the loop with your Rust code (the unavoidable "step 4")

As covered in `comparison3.md`, Atlas doesn't read Diesel/SeaORM model code, so after step 3 you sync your Rust types from the **dev** database (not production):

```bash
# Diesel
diesel print-schema --database-url "$DEV_DATABASE_URL" > src/schema.rs

# SeaORM
sea-orm-cli generate entity --database-url "$DEV_DATABASE_URL" -o src/entities
```

Full loop for this project: **edit `schema.sql` → `atlas migrate diff` → `atlas migrate apply` → regenerate Rust types**. Three of those four steps map directly onto Alembic's three; the fourth is the price of `schema.sql` (not Rust code) being the actual source of truth.

---

## 11. Summary checklist for adopting Atlas on these two backends

1. `curl -sSf https://atlasgo.sh | sh`
2. Write `schema.sql` (Postgres) and `schema_sqlite.sql` (SQLite) describing current desired state.
3. Write `atlas.hcl` with `postgres` and `sqlite` envs as shown in §4.
4. `atlas migrate diff initial_schema --env postgres` and `--env sqlite` to bootstrap migration directories from an empty dev DB.
5. `atlas migrate apply --env postgres` / `--env sqlite` against your real databases (use `atlas migrate import` if you already have an existing migration history from Alembic/Diesel/SeaORM you want to carry over instead of starting fresh).
6. Add `atlas migrate lint --latest 1` as a CI gate.
7. After every schema change: edit `schema.sql` → `migrate diff` → `migrate apply` → regenerate Rust types from the dev DB.
