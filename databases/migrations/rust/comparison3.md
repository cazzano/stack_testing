# Alembic vs Atlas — and how Atlas fits a Rust project

## 1. What Atlas actually is

Atlas (atlasgo.io) is a **standalone, language-agnostic CLI** (written in Go, distributed as a single binary). It is not an ORM and has no Rust integration of its own. What it does:

- Takes a "desired state" schema, expressed as **plain SQL**, **Atlas HCL** (Terraform-like DSL), or an **ORM loader** (officially supports SQLAlchemy, GORM, Django, Hibernate, EF Core, Drizzle, Sequelize, TypeORM, Prisma, Ent — **no official Diesel/SeaORM/SQLx loader exists**).
- Spins up a throwaway "dev database" (Docker container) to safely compute diffs.
- Diffs the desired state against either a live database or a directory of previously-applied migrations.
- Writes a versioned SQL migration file containing the diff (`atlas migrate diff`).
- Applies migrations (`atlas migrate apply`) and tracks history in its own table (`atlas_schema_revisions`).
- Supports Postgres, SQLite, MySQL, and many others — **same binary, same commands, for both your Postgres and SQLite backends**.

Because there's no Rust ORM loader, the realistic "source of truth" for a Rust project is a **plain `schema.sql` file** (or Atlas HCL) that you maintain by hand, separate from your Rust structs — *not* your Diesel/SeaORM model code directly.

## 2. The 3 legendary steps, mapped onto Atlas

| Step | Alembic | Atlas (Rust project) |
|---|---|---|
| **1. Define the change** | Edit `schema.py` (SQLAlchemy models) | Edit `schema.sql` (plain `CREATE TABLE` statements) — this is your new "single source of truth" |
| **2. Generate** | `alembic revision --autogenerate -m "..."` | `atlas migrate diff add_lock_file_column --to file://schema.sql --dev-url "docker://postgres/16/dev"` |
| **3. Apply** | `alembic upgrade head` | `atlas migrate apply --url "$DATABASE_URL"` |

This is structurally **identical** to Alembic's loop — edit a declarative schema file, get a diff generated for you, apply it. It's actually the closest match of the three options compared so far (sea-orm-migration, Diesel, Atlas).

## 3. Worked example

**Alembic**
```python
# 1. schema.py
class ClinicDevices(Base, TimestampMixin):
    ...
    lock_file = Column(Text, nullable=True)
```
```bash
# 2. generate
alembic revision --autogenerate -m "add lock_file column"
# 3. apply
alembic upgrade head
```

**Atlas**
```sql
-- 1. schema.sql
CREATE TABLE clinic_devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_guid TEXT,
    ...
    lock_file TEXT,
    clinic_id UUID NOT NULL REFERENCES clinics(id)
);
```
```bash
# 2. generate (diffs migrations/ dir vs schema.sql using a disposable dev container)
atlas migrate diff add_lock_file_column \
  --dir "file://migrations" \
  --to "file://schema.sql" \
  --dev-url "docker://postgres/16/dev"

# -> writes migrations/20260616120000_add_lock_file_column.sql containing:
#    ALTER TABLE "clinic_devices" ADD COLUMN "lock_file" text NULL;

# 3. apply
atlas migrate apply --dir "file://migrations" --url "$DATABASE_URL"
```

## 4. Config: `atlas.hcl`

A minimal config that supports both your backends, using environments:

```hcl
env "postgres" {
  src = "file://schema.sql"
  url = env("PG_DATABASE_URL")
  dev = "docker://postgres/16/dev"
  migration {
    dir = "file://migrations/postgres"
  }
}

env "sqlite" {
  src = "file://schema.sql"
  url = env("SQLITE_DATABASE_URL")  // e.g. sqlite://app.db
  dev = "sqlite://file?mode=memory"
  migration {
    dir = "file://migrations/sqlite"
  }
}
```

Then: `atlas migrate diff --env postgres ...` / `atlas migrate diff --env sqlite ...`. Same source schema, two separate migration directories (because Postgres-only DDL like `gen_random_uuid()` or generated columns won't translate to SQLite — same caveat as every other tool discussed).

## 5. Where Atlas wins vs Alembic

| | Alembic | Atlas |
|---|---|---|
| Multi-database support (Postgres + SQLite) with one tool | No — Python/SQLAlchemy only | Yes — same binary/CLI for both |
| Pre-check "is DB in sync" | `alembic check` | `atlas migrate lint` / `atlas schema diff` (no-op if in sync) |
| Migration safety analysis | None built-in | 50+ built-in linters: detects destructive changes, locking operations, data-dependent changes, backward-incompatible changes |
| Declarative "apply directly" mode (Terraform-style) | No — always versioned files | Yes — `atlas schema apply` reconciles DB to desired state directly, in addition to versioned migrations |
| CI/CD integrations | Roll your own | GitHub Actions, GitLab CI, Kubernetes operator, Terraform provider out of the box |
| Drift detection | None | Built-in (`atlas schema inspect` + drift monitoring) |

## 6. Where Atlas loses vs Alembic (for this Rust setup specifically)

| | Alembic | Atlas |
|---|---|---|
| Source of truth = your actual model code | Yes — `schema.py` *is* the SQLAlchemy models used at runtime | No — `schema.sql` is a **separate file** from your Diesel `schema.rs` / SeaORM entities. You maintain two representations: the SQL schema (for Atlas) and the Rust types (for your app) |
| Risk of drift between "source of truth" and Rust code | N/A | Real — if you edit `schema.sql` and forget to regenerate/update your Rust structs (or vice versa), they silently diverge until a query fails |
| Tooling maturity for this exact use case | Native, first-party | Workable but bolted-on; no official Rust loader as of writing |
| New dependency to install/learn | None (already Python ecosystem) | A new Go binary, new HCL syntax (if you use Atlas DDL instead of plain SQL), new CI step |

## 7. Closing the gap: keeping `schema.sql` and Rust types in sync

Since Atlas can't read Diesel/SeaORM code directly, the practical pattern is:

1. `schema.sql` is the canonical source of truth (edited by hand).
2. Atlas generates and applies migrations from it (steps 2–3 above).
3. After `atlas migrate apply` runs against your **dev** database, run your ORM's reverse-codegen against that same dev DB:
   - Diesel: `diesel print-schema > src/schema.rs`
   - SeaORM: `sea-orm-cli generate entity -o src/entities`

So the *full* loop becomes 4 steps instead of 3 — Atlas handles the DB-facing 3 steps cleanly (matching Alembic 1:1), but you bolt on a 4th step to resync your Rust code, which Alembic doesn't need because Python models *are* the source of truth.

## 8. Bottom line

- **Structurally**, Atlas is the closest match to Alembic's "edit declarative schema → autogenerate diff → apply" workflow of all the options considered, and it's the only one that works identically across both your Postgres and SQLite backends with one tool.
- **Practically**, it introduces a split between "the schema Atlas knows about" (`schema.sql`/HCL) and "the schema your Rust code knows about" (`schema.rs` / SeaORM entities), which Alembic avoids entirely since `schema.py` serves both roles.
- It's the right choice if: you want strong migration safety linting, CI/CD integration, and a single cross-database tool, and you're willing to treat `schema.sql` as the real source of truth with Rust types as a generated/derived artifact.
- It's probably overkill if: your team would rather keep "the schema" living in one place (Rust code) even if that means more manual migration writing (→ Diesel/SeaORM as discussed in comparison.md and comparison2.md).
